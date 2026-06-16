#!/usr/bin/env python3
"""Entropic regularization of optimal transport and its epsilon-limit (numerical demo).

This script numerically reproduces the epsilon-limit convergence theorem for the
entropic-regularized Kantorovich problem (seminar ch.04, Thm 4.13,
``thm:sem-entropic-convergence-eps-zero``):

    (i)   lim_{eps -> 0}  MK^eps_C(a, b) = MK_C(a, b)          (optimal value)
    (ii)  P_eps -> argmax_{P in S*} H(P)  as eps -> 0          (max-entropy selection)
    (iii) P_eps -> a b^T                  as eps -> +infty     (independent coupling)

The regularized plan P_eps is computed with the matrix-scaling iteration that
realizes the scaling form  P_eps = diag(u) K diag(v)  of Prop. 4.9
(``prop:sem-entropic-scaling-form``); the iteration is used here as a black-box
solver -- its convergence-rate analysis (Hilbert metric / Birkhoff, ch.05) is out
of scope. The iteration is run in the log-domain so that small eps does not
underflow the Gibbs kernel K = exp(-C/eps).

Pure Python + numpy. matplotlib is optional (only for the PDF figures).

Reference: Peyre & Cuturi, "Computational Optimal Transport" (2019).
"""

import argparse
import itertools
import os

import numpy as np

try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    HAS_MPL = True
except ImportError:  # figures are optional; the numerical report always runs
    HAS_MPL = False


# ---------------------------------------------------------------------------
# Functionals on transport plans (definitions of ch.04)
# ---------------------------------------------------------------------------

def transport_cost(C, P):
    """Frobenius inner product <C, P> = sum_ij C_ij P_ij."""
    return float(np.sum(C * P))


def entropy(P):
    """Discrete entropy H(P) = -sum_ij P_ij (log P_ij - 1), with 0 log 0 = 0 (Def. 4.1)."""
    mask = P > 0
    return float(-np.sum(P[mask] * (np.log(P[mask]) - 1.0)))


def gibbs_kernel(C, eps):
    """Gibbs kernel K = exp(-C/eps) (Def. 4.7). May underflow for small eps."""
    return np.exp(-C / eps)


def kl_divergence(P, K):
    """KL(P || K) = sum_ij (P log(P/K) - P + K) (Def. 4.6), with 0 log 0 = 0."""
    mask = P > 0
    val = np.sum(P[mask] * np.log(P[mask] / K[mask]) - P[mask] + K[mask])
    val += np.sum(K[~mask])  # the P = 0 entries contribute +K_ij
    return float(val)


def reg_objective(C, P, eps):
    """Regularized objective <C, P> - eps H(P); equals MK^eps_C at the optimum."""
    return transport_cost(C, P) - eps * entropy(P)


# ---------------------------------------------------------------------------
# Cost matrix
# ---------------------------------------------------------------------------

def cost_matrix_1d(x, y, p=2):
    """Ground cost C_ij = |x_i - y_j|^p on the line."""
    return np.abs(x[:, None] - y[None, :]) ** p


# ---------------------------------------------------------------------------
# Matrix-scaling iteration (= Sinkhorn), log-domain (stable form of Prop. 4.9)
# ---------------------------------------------------------------------------

def _logsumexp(M, axis):
    """Numerically stable log-sum-exp along an axis (pure numpy)."""
    m = np.max(M, axis=axis, keepdims=True)
    out = m + np.log(np.sum(np.exp(M - m), axis=axis, keepdims=True))
    return np.squeeze(out, axis=axis)


def sinkhorn(C, a, b, eps, n_iter=20000, tol=1e-12):
    """Solve P_eps = argmin_{P in U(a,b)} <C,P> - eps H(P) by matrix scaling.

    Log-domain implementation. We carry potentials f in R^n, g in R^m (the
    f = eps*alpha, g = eps*beta of Rem. 4.11), so that the scaling vectors are
    u = exp(f/eps), v = exp(g/eps) and the plan is

        P_ij = u_i K_ij v_j = exp((f_i + g_j - C_ij)/eps).

    The standard iteration u <- a / (K v), v <- b / (K^T u) becomes

        f_i <- eps log a_i - eps logsumexp_j (g_j - C_ij)/eps
        g_j <- eps log b_j - eps logsumexp_i (f_i - C_ij)/eps

    Returns (P, info) where info holds the iteration count and marginal residual.
    """
    log_a = np.log(a)
    log_b = np.log(b)
    f = np.zeros(len(a))
    g = np.zeros(len(b))  # g = 0  <=>  v = 1  (the standard initialization)

    resid = np.inf
    it = 0
    for it in range(1, n_iter + 1):
        f = eps * (log_a - _logsumexp((g[None, :] - C) / eps, axis=1))
        g = eps * (log_b - _logsumexp((f[:, None] - C) / eps, axis=0))
        # The g-update makes the column marginal exact; check the row marginal.
        P = np.exp((f[:, None] + g[None, :] - C) / eps)
        resid = float(np.sum(np.abs(P.sum(axis=1) - a)) + np.sum(np.abs(P.sum(axis=0) - b)))
        if resid < tol:
            break

    P = np.exp((f[:, None] + g[None, :] - C) / eps)
    info = {"iterations": it, "marginal_residual": resid, "f": f, "g": g}
    return P, info


# ---------------------------------------------------------------------------
# Exact unregularized OT (pure numpy), used as the eps -> 0 reference of (i)
# ---------------------------------------------------------------------------

def north_west_corner(a, b):
    """Monotone coupling via the north-west corner rule.

    For sorted 1D supports and a convex ground cost, this monotone plan is the
    exact Kantorovich optimum, so <C, P_NW> = MK_C(a, b) (no LP needed).
    """
    n, m = len(a), len(b)
    ra, rb = a.copy(), b.copy()
    P = np.zeros((n, m))
    i = j = 0
    eps0 = 1e-15
    while i < n and j < m:
        t = min(ra[i], rb[j])
        P[i, j] = t
        ra[i] -= t
        rb[j] -= t
        if ra[i] <= eps0 and i < n - 1:
            i += 1
        elif rb[j] <= eps0 and j < m - 1:
            j += 1
        else:
            break
    return P


def brute_force_ot(C, a, b):
    """Exact OT cost for the n x n uniform (a = b = 1/n) case by enumerating
    the vertices of U(a,b), which are (1/n) * permutation matrices."""
    n = len(a)
    assert n == len(b) and np.allclose(a, 1.0 / n) and np.allclose(b, 1.0 / n)
    best_cost, best_perm = np.inf, None
    for perm in itertools.permutations(range(n)):
        cost = sum(C[i, perm[i]] for i in range(n)) / n
        if cost < best_cost - 1e-15:
            best_cost, best_perm = cost, perm
    return best_cost, best_perm


# ---------------------------------------------------------------------------
# Problem instances
# ---------------------------------------------------------------------------

def gaussian_mixture(grid, centers, widths, weights):
    """Normalized histogram of a 1D Gaussian mixture sampled on ``grid``."""
    h = np.zeros_like(grid)
    for c, w, wt in zip(centers, widths, weights):
        h += wt * np.exp(-0.5 * ((grid - c) / w) ** 2)
    return h / h.sum()


def make_1d_problem(n, m):
    """Two 1D mixture histograms on [0,1] with squared-distance cost."""
    x = np.linspace(0.0, 1.0, n)
    y = np.linspace(0.0, 1.0, m)
    a = gaussian_mixture(x, centers=[0.2, 0.6], widths=[0.06, 0.08], weights=[0.6, 0.4])
    b = gaussian_mixture(y, centers=[0.4, 0.85], widths=[0.07, 0.05], weights=[0.5, 0.5])
    C = cost_matrix_1d(x, y, p=2)
    return x, y, a, b, C


def make_degenerate_problem():
    """3x3 instance whose unregularized OT has *multiple* optima (Thm 4.13 (ii)).

    a = b = (1/3,1/3,1/3); cost has two tied optimal permutations (identity and
    the (0 1) transposition), both of cost 0. The optimal face S* is the
    1-parameter family with a free 2x2 block in the top-left corner, and

        P_star = argmax_{S*} H = [[1/6,1/6, 0 ],
                                  [1/6,1/6, 0 ],
                                  [ 0 , 0 ,1/3]].
    """
    a = np.full(3, 1.0 / 3.0)
    b = np.full(3, 1.0 / 3.0)
    C = np.array([[0.0, 0.0, 1.0],
                  [0.0, 0.0, 1.0],
                  [1.0, 1.0, 0.0]])
    P_star = np.array([[1.0 / 6, 1.0 / 6, 0.0],
                       [1.0 / 6, 1.0 / 6, 0.0],
                       [0.0, 0.0, 1.0 / 3]])
    return a, b, C, P_star


# ---------------------------------------------------------------------------
# Console report
# ---------------------------------------------------------------------------

def _rule(title):
    print("\n" + "=" * 72)
    print(title)
    print("=" * 72)


def sweep_1d(C, a, b, eps_grid, n_iter, tol):
    """Run the matrix-scaling solver across an eps grid; collect diagnostics."""
    product = np.outer(a, b)
    rows = []
    for eps in eps_grid:
        P, info = sinkhorn(C, a, b, eps, n_iter=n_iter, tol=tol)
        rows.append({
            "eps": eps,
            "P": P,
            "cost": transport_cost(C, P),
            "reg": reg_objective(C, P, eps),
            "H": entropy(P),
            "resid": info["marginal_residual"],
            "iters": info["iterations"],
            "dist_product": float(np.sum(np.abs(P - product))),
        })
    return rows


def report_1d(rows, mk_C, cost_product):
    """(i) value convergence to MK_C and (iii) convergence to a b^T."""
    _rule("[ (i) eps -> 0 ]  optimal value converges to the true OT cost")
    print(f"  true OT cost  MK_C(a,b)        = {mk_C:.8f}   (north-west corner, exact)")
    print(f"  product cost  <C, a b^T>       = {cost_product:.8f}   (eps -> +inf reference)")
    print()
    print("    eps        <C,P_eps>     MK^eps_C       gap=<C,P_eps>-MK_C    H(P_eps)   iters  resid")
    print("    " + "-" * 92)
    for r in rows:
        print(f"    {r['eps']:9.4g}  {r['cost']:11.6f}  {r['reg']:12.6f}  "
              f"{r['cost'] - mk_C:18.2e}  {r['H']:9.4f}  {r['iters']:6d}  {r['resid']:.1e}")
    print("\n  -> as eps decreases, <C,P_eps> and MK^eps_C both approach MK_C (gap -> 0).")

    _rule("[ (iii) eps -> +inf ]  plan converges to the independent coupling a b^T")
    print("    eps          || P_eps - a b^T ||_1")
    print("    " + "-" * 42)
    for r in rows:
        if r["eps"] >= 1.0:
            print(f"    {r['eps']:9.4g}    {r['dist_product']:.3e}")
    print("\n  -> as eps grows, P_eps -> a b^T (mass spreads to the product / independence).")


def _fmt_matrix(M):
    return "\n".join("      [" + "  ".join(f"{v:7.4f}" for v in row) + "]" for row in M)


def report_degenerate(a, b, C, P_star, eps_list, n_iter, tol):
    """(ii) entropy-maximizing selection among multiple optima."""
    _rule("[ (ii) eps -> 0 ]  entropic reg. selects the max-entropy optimum")
    mk_C, perm = brute_force_ot(C, a, b)
    print(f"  true OT cost MK_C = {mk_C:.6f}  (>=2 tied optimal permutations => multiple optima)")
    print(f"  analytic max-entropy optimum  P* = argmax_(S*) H,  H(P*) = {entropy(P_star):.5f}:")
    print(_fmt_matrix(P_star))
    # A vertex of the optimal face (a *non*-max-entropy optimum) for contrast.
    P_vertex = np.array([[1.0 / 3, 0.0, 0.0], [0.0, 1.0 / 3, 0.0], [0.0, 0.0, 1.0 / 3]])
    print(f"  (contrast) an optimal vertex P_id has lower entropy  H = {entropy(P_vertex):.5f}")
    print()
    print("    eps        <C,P_eps>     H(P_eps)    ||P_eps - P*||_max")
    print("    " + "-" * 58)
    last_P = None
    for eps in eps_list:
        P, _ = sinkhorn(C, a, b, eps, n_iter=n_iter, tol=tol)
        diff = float(np.max(np.abs(P - P_star)))
        print(f"    {eps:9.4g}  {transport_cost(C, P):11.6f}  {entropy(P):9.5f}  {diff:18.2e}")
        last_P = P
    print("\n  P_eps at the smallest eps:")
    print(_fmt_matrix(last_P))
    print("\n  -> P_eps -> P*: the top-left 2x2 block fills uniformly to 1/6, (2,2) -> 1/3.")
    print("     H(P_eps) >= H(P*) for every eps>0 and decreases toward H(P*) as eps -> 0.")


def report_sanity(C, a, b):
    """Cross-checks of the ch.04 structure (scaling form, KL projection)."""
    _rule("[ sanity ]  scaling form P_eps = diag(u) K diag(v) and KL projection")
    eps = 0.05  # moderate eps so that K = exp(-C/eps) does not underflow
    P, info = sinkhorn(C, a, b, eps)
    K = gibbs_kernel(C, eps)
    u = np.exp(info["f"] / eps)
    v = np.exp(info["g"] / eps)
    P_scaled = u[:, None] * K * v[None, :]
    print(f"  eps = {eps}")
    print(f"  || P_eps - diag(u) K diag(v) ||_max = {np.max(np.abs(P - P_scaled)):.2e}  (Prop. 4.9)")
    print(f"  row-marginal residual ||P1 - a||_1  = {np.sum(np.abs(P.sum(1) - a)):.2e}")
    print(f"  col-marginal residual ||P^T1 - b||_1= {np.sum(np.abs(P.sum(0) - b)):.2e}")
    print(f"  KL(P_eps || K)                      = {kl_divergence(P, K):.6f}  (Prop. 4.8: P_eps = argmin KL(.||K))")


# ---------------------------------------------------------------------------
# Figures (matplotlib, optional)
# ---------------------------------------------------------------------------

def plot_eps_sweep_plans(rows, P_NW, product, output_dir):
    eps_show = [0.001, 0.005, 0.02, 0.1, 0.5, 5.0]
    panels = [("true OT  P_NW", P_NW)]
    for eps in eps_show:
        r = min(rows, key=lambda rr: abs(np.log(rr["eps"]) - np.log(eps)))
        panels.append((f"eps = {r['eps']:.3g}", r["P"]))
    panels.append(("product  a b^T", product))

    ncol = 4
    nrow = int(np.ceil(len(panels) / ncol))
    fig, axes = plt.subplots(nrow, ncol, figsize=(3.2 * ncol, 3.0 * nrow))
    axes = np.atleast_1d(axes).ravel()
    for ax, (title, M) in zip(axes, panels):
        ax.imshow(M, origin="upper", cmap="magma", aspect="auto")
        ax.set_title(title, fontsize=10)
        ax.set_xticks([])
        ax.set_yticks([])
    for ax in axes[len(panels):]:
        ax.axis("off")
    fig.suptitle("Entropic OT plan $P_\\varepsilon$: from true OT ($\\varepsilon\\to0$) "
                 "to independence ($\\varepsilon\\to\\infty$)", fontsize=12)
    fig.tight_layout(rect=(0, 0, 1, 0.96))
    path = os.path.join(output_dir, "eps_sweep_plans.pdf")
    fig.savefig(path)
    plt.close(fig)
    print(f"  saved {path}")


def plot_cost_entropy(rows, mk_C, cost_product, h_product, output_dir):
    eps = np.array([r["eps"] for r in rows])
    cost = np.array([r["cost"] for r in rows])
    reg = np.array([r["reg"] for r in rows])
    H = np.array([r["H"] for r in rows])

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.2))
    ax1.semilogx(eps, cost, "o-", label=r"$\langle C, P_\varepsilon\rangle$")
    ax1.semilogx(eps, reg, "s--", label=r"$MK^\varepsilon_C$")
    ax1.axhline(mk_C, color="green", ls=":", label=r"$MK_C$  ($\varepsilon\to0$)")
    ax1.axhline(cost_product, color="red", ls=":", label=r"$\langle C, ab^\top\rangle$  ($\varepsilon\to\infty$)")
    ax1.set_xlabel(r"$\varepsilon$")
    ax1.set_ylabel("cost")
    ax1.set_title("(i) value converges to $MK_C$ as $\\varepsilon\\to0$")
    ax1.legend(fontsize=8)

    ax2.semilogx(eps, H, "o-", color="purple", label=r"$H(P_\varepsilon)$")
    ax2.axhline(h_product, color="red", ls=":", label=r"$H(ab^\top)$ (max)")
    ax2.set_xlabel(r"$\varepsilon$")
    ax2.set_ylabel("entropy")
    ax2.set_title("entropy increases with $\\varepsilon$ toward the product")
    ax2.legend(fontsize=8)

    fig.tight_layout()
    path = os.path.join(output_dir, "cost_entropy_vs_eps.pdf")
    fig.savefig(path)
    plt.close(fig)
    print(f"  saved {path}")


def plot_maxent_selection(a, b, C, P_star, eps_list, output_dir, n_iter, tol):
    panels = []
    for eps in eps_list:
        P, _ = sinkhorn(C, a, b, eps, n_iter=n_iter, tol=tol)
        panels.append((f"eps = {eps:g}", P))
    panels.append(("analytic  $P^\\star$", P_star))

    fig, axes = plt.subplots(1, len(panels), figsize=(2.6 * len(panels), 2.8))
    for ax, (title, M) in zip(axes, panels):
        ax.imshow(M, origin="upper", cmap="viridis", vmin=0, vmax=1.0 / 3)
        for i in range(M.shape[0]):
            for j in range(M.shape[1]):
                ax.text(j, i, f"{M[i, j]:.2f}", ha="center", va="center",
                        color="white" if M[i, j] < 0.22 else "black", fontsize=8)
        ax.set_title(title, fontsize=10)
        ax.set_xticks([])
        ax.set_yticks([])
    fig.suptitle("(ii) max-entropy selection among multiple optima: "
                 "$P_\\varepsilon \\to P^\\star$", fontsize=12)
    fig.tight_layout(rect=(0, 0, 1, 0.93))
    path = os.path.join(output_dir, "maxent_selection.pdf")
    fig.savefig(path)
    plt.close(fig)
    print(f"  saved {path}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main(args):
    np.random.seed(args.seed)
    os.makedirs(args.output_dir, exist_ok=True)

    print("[1/5] Building 1D problem (Gaussian-mixture histograms) ...")
    x, y, a, b, C = make_1d_problem(args.n, args.m)
    product = np.outer(a, b)
    P_NW = north_west_corner(a, b)
    mk_C = transport_cost(C, P_NW)
    cost_product = transport_cost(C, product)
    h_product = entropy(product)
    print(f"      n = {args.n}, m = {args.m}, cost = squared distance on [0,1]")

    print("[2/5] Running matrix-scaling solver across the eps grid ...")
    eps_grid = np.logspace(np.log10(args.eps_min), np.log10(args.eps_max), args.n_eps)
    rows = sweep_1d(C, a, b, eps_grid, args.n_iter, args.tol)

    print("[3/5] Reporting (i) value convergence and (iii) independence limit ...")
    report_1d(rows, mk_C, cost_product)

    print("\n[4/5] Reporting (ii) max-entropy selection on the degenerate 3x3 ...")
    da, db, dC, P_star = make_degenerate_problem()
    deg_eps = [1.0, 0.2, 0.05, 0.01]
    report_degenerate(da, db, dC, P_star, deg_eps, args.n_iter, args.tol)
    report_sanity(C, a, b)

    if args.no_plots or not HAS_MPL:
        if args.no_plots:
            print("\n[5/5] Figures skipped (--no-plots).")
        else:
            print("\n[5/5] Figures skipped (matplotlib not available). Install it for PDFs.")
        return

    print("\n[5/5] Writing figures ...")
    plot_eps_sweep_plans(rows, P_NW, product, args.output_dir)
    plot_cost_entropy(rows, mk_C, cost_product, h_product, args.output_dir)
    plot_maxent_selection(da, db, dC, P_star, deg_eps, args.output_dir, args.n_iter, args.tol)


def build_parser():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--n", type=int, default=50, help="size of source histogram (1D demo)")
    p.add_argument("--m", type=int, default=50, help="size of target histogram (1D demo)")
    p.add_argument("--seed", type=int, default=0)
    p.add_argument("--output-dir", type=str,
                   default=os.path.join(os.path.dirname(__file__), "out"),
                   help="directory for the PDF figures")
    p.add_argument("--eps-min", type=float, default=1e-3, help="smallest eps in the sweep")
    p.add_argument("--eps-max", type=float, default=1e2, help="largest eps in the sweep")
    p.add_argument("--n-eps", type=int, default=19, help="number of eps values in the sweep")
    p.add_argument("--n-iter", type=int, default=20000, help="max matrix-scaling iterations")
    p.add_argument("--tol", type=float, default=1e-12, help="marginal-residual tolerance")
    p.add_argument("--no-plots", action="store_true", help="skip matplotlib figures")
    return p


if __name__ == "__main__":
    main(build_parser().parse_args())
