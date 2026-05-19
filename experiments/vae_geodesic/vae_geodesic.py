#!/usr/bin/env python3
"""VAE latent-space geodesics via pullback Riemannian metrics on MNIST (3D latent space).

Reference: Roy & Hauberg, "Optimal Latent Transport", NeurReps 2022.
"""

import argparse
import base64
import io
import json
import os

import matplotlib.pyplot as plt
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from PIL import Image
from scipy.optimize import minimize
from sklearn.datasets import fetch_openml
from torch.utils.data import DataLoader, TensorDataset


# ---------------------------------------------------------------------------
# Data
# ---------------------------------------------------------------------------

def load_mnist():
    mnist = fetch_openml("mnist_784", version=1, as_frame=False, parser="auto")
    X = mnist.data.astype(np.float32) / 255.0
    y = mnist.target.astype(np.int64)
    return X[:60000], y[:60000], X[60000:], y[60000:]


# ---------------------------------------------------------------------------
# Model
# ---------------------------------------------------------------------------

class Encoder(nn.Module):
    def __init__(self, data_dim=784, hidden_dim=512, latent_dim=3):
        super().__init__()
        self.body = nn.Sequential(
            nn.Linear(data_dim, hidden_dim), nn.GELU(),
            nn.Linear(hidden_dim, hidden_dim // 2), nn.GELU(),
        )
        self.fc_mu = nn.Linear(hidden_dim // 2, latent_dim)
        self.fc_logvar = nn.Linear(hidden_dim // 2, latent_dim)

    def forward(self, x):
        h = self.body(x)
        return self.fc_mu(h), self.fc_logvar(h)


class Decoder(nn.Module):
    def __init__(self, latent_dim=3, hidden_dim=256, data_dim=784):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(latent_dim, hidden_dim), nn.GELU(),
            nn.Linear(hidden_dim, hidden_dim * 2), nn.GELU(),
            nn.Linear(hidden_dim * 2, data_dim), nn.Sigmoid(),
        )

    def forward(self, z):
        return self.net(z)


class VAE(nn.Module):
    def __init__(self, data_dim=784, hidden_dim=512, latent_dim=3):
        super().__init__()
        self.encoder = Encoder(data_dim, hidden_dim, latent_dim)
        self.decoder = Decoder(latent_dim, hidden_dim // 2, data_dim)

    def reparameterize(self, mu, logvar):
        std = torch.exp(0.5 * logvar)
        return mu + std * torch.randn_like(std)

    def forward(self, x):
        mu_z, logvar_z = self.encoder(x)
        z = self.reparameterize(mu_z, logvar_z)
        mu_x = self.decoder(z)
        return mu_x, mu_z, logvar_z

    def loss(self, x, mu_x, mu_z, logvar_z):
        recon = F.binary_cross_entropy(mu_x, x, reduction="none").sum(dim=-1)
        kl = -0.5 * torch.sum(1 + logvar_z - mu_z ** 2 - logvar_z.exp(),
                               dim=-1)
        return (recon + kl).mean()


# ---------------------------------------------------------------------------
# Training
# ---------------------------------------------------------------------------

def train_vae(model, loader, epochs, lr, device):
    model.to(device)
    opt = torch.optim.Adam(model.parameters(), lr=lr)
    model.train()
    for epoch in range(1, epochs + 1):
        total_loss = 0.0
        for (xb,) in loader:
            xb = xb.to(device)
            mu_x, mu_z, logvar_z = model(xb)
            loss = model.loss(xb, mu_x, mu_z, logvar_z)
            opt.zero_grad()
            loss.backward()
            opt.step()
            total_loss += loss.item() * xb.size(0)
        if epoch % 10 == 0 or epoch == 1:
            print(f"  epoch {epoch:3d}/{epochs}  loss={total_loss / len(loader.dataset):.2f}")
    return model


# ---------------------------------------------------------------------------
# Metric tensors
# ---------------------------------------------------------------------------

def _jacobian_mu(decoder, z):
    eps = 1e-4
    d = z.shape[0]
    with torch.no_grad():
        f0 = decoder(z.unsqueeze(0)).squeeze(0)
        J = torch.zeros(f0.shape[0], d, device=z.device)
        for i in range(d):
            z_p = z.clone()
            z_p[i] += eps
            f_p = decoder(z_p.unsqueeze(0)).squeeze(0)
            J[:, i] = (f_p - f0) / eps
    return J


def pullback_metric_at(decoder, z, eps_reg=1e-6):
    J = _jacobian_mu(decoder, z)
    d = z.shape[0]
    return J.T @ J + eps_reg * torch.eye(d, device=z.device)


# ---------------------------------------------------------------------------
# Grid-based metric interpolation (n-linear, works for any dimension)
# ---------------------------------------------------------------------------

class MetricGrid:
    def __init__(self, decoder, z_min, z_max, grid_n, metric_fn, device):
        d = len(z_min)
        self.d = d
        self.grid_n = grid_n
        self.vals = [np.linspace(z_min[i], z_max[i], grid_n) for i in range(d)]
        self.grid = np.zeros(tuple([grid_n] * d) + (d, d))

        decoder.eval()
        total = grid_n ** d
        with torch.no_grad():
            for count, idx in enumerate(np.ndindex(*([grid_n] * d))):
                z_np = np.array([self.vals[i][idx[i]] for i in range(d)],
                                dtype=np.float32)
                z = torch.tensor(z_np, device=device)
                G = metric_fn(decoder, z).cpu().numpy()
                self.grid[idx] = G
                if (count + 1) % 2000 == 0:
                    print(f"    {count + 1}/{total}")

    def __call__(self, z_np):
        f = np.empty(self.d)
        for i in range(self.d):
            span = self.vals[i][-1] - self.vals[i][0]
            f[i] = np.clip(
                (z_np[i] - self.vals[i][0]) / span * (self.grid_n - 1),
                0, self.grid_n - 1.001)

        i0 = np.floor(f).astype(int)
        df = f - i0

        G = np.zeros((self.d, self.d))
        for corner in range(1 << self.d):
            idx = tuple(min(i0[j] + ((corner >> j) & 1), self.grid_n - 1)
                        for j in range(self.d))
            w = 1.0
            for j in range(self.d):
                w *= df[j] if ((corner >> j) & 1) else (1 - df[j])
            G += w * self.grid[idx]
        return G


# ---------------------------------------------------------------------------
# Geodesic solver
# ---------------------------------------------------------------------------

def compute_geodesic(metric_grid, z_start, z_end, K=30):
    d = z_start.shape[0]

    def energy_and_grad(w_flat):
        waypoints = w_flat.reshape(K, d)
        path = np.vstack([z_start[None], waypoints, z_end[None]])
        E = 0.0
        grad = np.zeros_like(waypoints)
        for k in range(K + 1):
            dz = path[k + 1] - path[k]
            mid = 0.5 * (path[k] + path[k + 1])
            G = metric_grid(mid)
            E += dz @ G @ dz
            Gdz = G @ dz
            if k < K:
                grad[k] += 2 * Gdz
            if k > 0:
                grad[k - 1] -= 2 * Gdz
        E *= (K + 1)
        grad *= (K + 1)
        return E, grad.ravel()

    t = np.linspace(0, 1, K + 2)[1:-1, None]
    w0 = (z_start + t * (z_end - z_start)).ravel()
    result = minimize(energy_and_grad, w0, method="L-BFGS-B", jac=True,
                      options={"maxiter": 500, "ftol": 1e-12, "gtol": 1e-8})
    waypoints = result.x.reshape(K, d)
    return np.vstack([z_start[None], waypoints, z_end[None]])


def curve_energy(metric_grid, path):
    K = len(path) - 1
    energy = 0.0
    for k in range(K):
        dz = path[k + 1] - path[k]
        mid = 0.5 * (path[k] + path[k + 1])
        G = metric_grid(mid)
        energy += dz @ G @ dz
    return energy * K


# ---------------------------------------------------------------------------
# Pair selection
# ---------------------------------------------------------------------------

def select_pairs(mu_z, y, pairs_spec):
    results = []
    for d1, d2 in pairs_spec:
        idx1 = np.where(y == d1)[0]
        idx2 = np.where(y == d2)[0]
        c1 = mu_z[idx1].mean(axis=0)
        c2 = mu_z[idx2].mean(axis=0)
        i1 = idx1[np.argmin(np.sum((mu_z[idx1] - c1) ** 2, axis=1))]
        i2 = idx2[np.argmin(np.sum((mu_z[idx2] - c2) ** 2, axis=1))]
        results.append((d1, d2, mu_z[i1], mu_z[i2]))
    return results


# ---------------------------------------------------------------------------
# Visualisation (3D)
# ---------------------------------------------------------------------------

def plot_latent_scatter(mu_z, y, output_dir):
    fig = plt.figure(figsize=(12, 5))
    cmap = plt.colormaps.get_cmap("tab10")
    for i, (elev, azim) in enumerate([(25, -60), (25, 30)]):
        ax = fig.add_subplot(1, 2, i + 1, projection="3d")
        for digit in range(10):
            mask = y == digit
            ax.scatter(mu_z[mask, 0], mu_z[mask, 1], mu_z[mask, 2],
                       s=0.5, alpha=0.3, c=[cmap(digit)], label=str(digit))
        ax.set_xlabel(r"$z_1$"); ax.set_ylabel(r"$z_2$"); ax.set_zlabel(r"$z_3$")
        ax.view_init(elev=elev, azim=azim)
        if i == 0:
            ax.legend(markerscale=8, fontsize=7, loc="upper left")
    fig.suptitle("Latent space (test set)", fontsize=12)
    fig.tight_layout()
    fig.savefig(os.path.join(output_dir, "ch05_latent_scatter.pdf"))
    plt.close(fig)
    print("  saved ch05_latent_scatter.pdf")


def plot_geodesic_paths(mu_z, y, pairs, paths_dict, output_dir):
    fig = plt.figure(figsize=(12, 5))
    cmap = plt.colormaps.get_cmap("tab10")
    for i, (elev, azim) in enumerate([(25, -60), (25, 30)]):
        ax = fig.add_subplot(1, 2, i + 1, projection="3d")
        for digit in range(10):
            mask = y == digit
            ax.scatter(mu_z[mask, 0], mu_z[mask, 1], mu_z[mask, 2],
                       s=0.3, alpha=0.1, c=[cmap(digit)])
        for idx, (d1, d2, _, _) in enumerate(pairs):
            key = (d1, d2)
            lin = paths_dict[key]["linear"]
            geo = paths_dict[key]["pullback"]
            label_l = "Linear" if idx == 0 else None
            label_g = "Geodesic" if idx == 0 else None
            ax.plot(lin[:, 0], lin[:, 1], lin[:, 2],
                    color="gray", ls="--", lw=2, label=label_l)
            ax.plot(geo[:, 0], geo[:, 1], geo[:, 2],
                    color="tab:blue", ls="-", lw=2, label=label_g)
            ax.scatter([lin[0, 0], lin[-1, 0]],
                       [lin[0, 1], lin[-1, 1]],
                       [lin[0, 2], lin[-1, 2]],
                       c="black", s=40, zorder=6, marker="o")
        ax.set_xlabel(r"$z_1$"); ax.set_ylabel(r"$z_2$"); ax.set_zlabel(r"$z_3$")
        ax.view_init(elev=elev, azim=azim)
        if i == 0:
            ax.legend(fontsize=9)
    fig.suptitle("Geodesics vs linear interpolation", fontsize=12)
    fig.tight_layout()
    fig.savefig(os.path.join(output_dir, "ch05_geodesic_paths.pdf"))
    plt.close(fig)
    print("  saved ch05_geodesic_paths.pdf")


def plot_decoded_geodesic(decoder, paths_dict, pair_key, device, output_dir):
    kinds = ["linear", "pullback"]
    labels = ["Linear", "Geodesic"]
    n_show = 10
    fig, axes = plt.subplots(2, n_show, figsize=(n_show * 1.2, 2.8))
    for row, (kind, lbl) in enumerate(zip(kinds, labels)):
        path = paths_dict[pair_key][kind]
        indices = np.linspace(0, len(path) - 1, n_show).astype(int)
        for col, idx in enumerate(indices):
            z = torch.tensor(path[idx], dtype=torch.float32, device=device)
            with torch.no_grad():
                img = decoder(z.unsqueeze(0)).cpu().numpy().reshape(28, 28)
            axes[row, col].imshow(img, cmap="gray", vmin=0, vmax=1)
            axes[row, col].axis("off")
        axes[row, 0].set_ylabel(lbl, fontsize=10, rotation=0, labelpad=55,
                                 va="center")
    d1, d2 = pair_key
    fig.suptitle(f"Decoded images along paths ({d1} → {d2})", fontsize=12)
    fig.tight_layout(rect=[0.06, 0, 1, 0.95])
    fig.savefig(os.path.join(output_dir, "ch05_decoded_geodesic.pdf"))
    plt.close(fig)
    print("  saved ch05_decoded_geodesic.pdf")


def plot_metric_volume(mu_z, y, metric_grid, output_dir):
    rng = np.random.RandomState(42)
    n_pts = min(2000, len(mu_z))
    idx = rng.choice(len(mu_z), size=n_pts, replace=False)
    pts = mu_z[idx]
    log_vol = np.array([
        0.5 * np.log(max(np.linalg.det(metric_grid(p)), 1e-30))
        for p in pts])

    fig = plt.figure(figsize=(12, 5))
    for i, (elev, azim) in enumerate([(25, -60), (25, 30)]):
        ax = fig.add_subplot(1, 2, i + 1, projection="3d")
        sc = ax.scatter(pts[:, 0], pts[:, 1], pts[:, 2],
                        c=log_vol, cmap="viridis", s=2, alpha=0.5)
        ax.set_xlabel(r"$z_1$"); ax.set_ylabel(r"$z_2$"); ax.set_zlabel(r"$z_3$")
        ax.view_init(elev=elev, azim=azim)
        if i == 1:
            fig.colorbar(sc, ax=ax, shrink=0.6,
                         label=r"$\log\sqrt{\det G}$")
    fig.suptitle(r"Volume distortion $\sqrt{\det G(z)}$", fontsize=12)
    fig.tight_layout()
    fig.savefig(os.path.join(output_dir, "ch05_metric_ellipses.pdf"))
    plt.close(fig)
    print("  saved ch05_metric_ellipses.pdf")


# ---------------------------------------------------------------------------
# Web data export
# ---------------------------------------------------------------------------

def _img_to_b64(arr_28x28):
    img = Image.fromarray((arr_28x28 * 255).astype(np.uint8))
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return base64.b64encode(buf.getvalue()).decode()


def export_web_data(decoder, mu_z, y, pairs, paths_dict,
                    metric_grid, device, output_dir):
    rng = np.random.RandomState(0)
    idx = rng.choice(len(mu_z), size=min(3000, len(mu_z)), replace=False)
    points = mu_z[idx]
    labels = y[idx].tolist()

    log_vol = []
    for p in points:
        det_G = max(np.linalg.det(metric_grid(p)), 1e-30)
        log_vol.append(float(0.5 * np.log(det_G)))

    geodesics = []
    for d1, d2, _, _ in pairs:
        key = (d1, d2)
        entry = {"pair": [d1, d2]}
        for kind in ("linear", "pullback"):
            path = paths_dict[key][kind]
            entry[kind] = path.tolist()
            n_img = 12
            idxs = np.linspace(0, len(path) - 1, n_img).astype(int)
            imgs = []
            for i in idxs:
                z = torch.tensor(path[i], dtype=torch.float32, device=device)
                with torch.no_grad():
                    img = decoder(z.unsqueeze(0)).cpu().numpy().reshape(28, 28)
                imgs.append(_img_to_b64(img))
            entry[f"{kind}_imgs"] = imgs
        geodesics.append(entry)

    data = {
        "dim": 3,
        "z_min": mu_z.min(axis=0).tolist(),
        "z_max": mu_z.max(axis=0).tolist(),
        "points": points.tolist(),
        "labels": labels,
        "log_volume": log_vol,
        "geodesics": geodesics,
    }
    out_path = os.path.join(output_dir, "vae_geodesic_data.json")
    with open(out_path, "w") as f:
        json.dump(data, f)
    print(f"  saved {out_path}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main(args):
    torch.manual_seed(args.seed)
    np.random.seed(args.seed)
    device = torch.device(args.device)
    os.makedirs(args.output_dir, exist_ok=True)

    print("[1/7] Loading MNIST ...")
    X_train, y_train, X_test, y_test = load_mnist()
    train_ds = TensorDataset(torch.tensor(X_train))
    train_loader = DataLoader(train_ds, batch_size=args.batch_size, shuffle=True)

    print("[2/7] Training VAE ...")
    model = VAE(latent_dim=args.latent_dim)
    model = train_vae(model, train_loader, args.epochs, args.lr, device)
    model.eval()
    model.cpu()
    decoder = model.decoder
    cpu = torch.device("cpu")

    print("[3/7] Encoding test set ...")
    with torch.no_grad():
        X_t = torch.tensor(X_test, device=cpu)
        mu_z_all, _ = model.encoder(X_t)
        mu_z_np = mu_z_all.numpy()

    print("[4/7] Precomputing metric grid ...")
    margin = 0.5
    z_min = mu_z_np.min(axis=0) - margin
    z_max = mu_z_np.max(axis=0) + margin
    grid_n = 20

    pb_grid = MetricGrid(decoder, z_min, z_max, grid_n,
                          pullback_metric_at, cpu)
    print("  metric grid done")

    print("[5/7] Computing geodesics ...")
    digit_pairs = [(0, 1), (3, 8), (4, 9)]
    pairs = select_pairs(mu_z_np, y_test, digit_pairs)

    paths_dict = {}
    for d1, d2, p1, p2 in pairs:
        K = 30
        linear_path = np.array([p1 + t * (p2 - p1)
                                for t in np.linspace(0, 1, K + 2)])
        print(f"  pair ({d1},{d2}): computing geodesic ...")
        geo = compute_geodesic(pb_grid, p1, p2, K=K)
        paths_dict[(d1, d2)] = {"linear": linear_path, "pullback": geo}

        e_lin = curve_energy(pb_grid, linear_path)
        e_geo = curve_energy(pb_grid, geo)
        pct = (1 - e_geo / e_lin) * 100
        print(f"    energy: linear={e_lin:.1f}  geodesic={e_geo:.1f}  ({pct:.1f}% lower)")

    print("[6/7] Generating figures ...")
    plot_latent_scatter(mu_z_np, y_test, args.output_dir)
    plot_geodesic_paths(mu_z_np, y_test, pairs, paths_dict, args.output_dir)
    plot_decoded_geodesic(decoder, paths_dict, digit_pairs[0], cpu,
                          args.output_dir)
    plot_metric_volume(mu_z_np, y_test, pb_grid, args.output_dir)

    print("[7/7] Exporting JSON for web visualization ...")
    export_web_data(decoder, mu_z_np, y_test, pairs, paths_dict,
                    pb_grid, cpu, args.output_dir)

    print("Done.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="VAE geodesics on MNIST")
    parser.add_argument("--epochs", type=int, default=50)
    parser.add_argument("--batch-size", type=int, default=128)
    parser.add_argument("--latent-dim", type=int, default=3)
    parser.add_argument("--lr", type=float, default=1e-3)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--output-dir", type=str, default="../../seminar/tex/fig")
    parser.add_argument("--device", type=str, default="cpu")
    args = parser.parse_args()
    main(args)
