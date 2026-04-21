"""砂山 → 行き先 シナリオの可視化.

seminar `ch02_ot_foundations.tex` の TikZ 図 (行 44–86 の 1D 配置, 行 505–538 の
Monge 写像 vs Kantorovich カップリング対比) に相当する matplotlib 版を提供する.
"""

from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes

from cot.core.scenario import SandpileScenario
from cot.core.types import MongeMap, Permutation, TransportPlan


def _x_flat(a: np.ndarray) -> np.ndarray:
    """1D 座標として表示するため, (n,) または (n, 1) を (n,) に正規化."""
    return a.reshape(-1) if a.ndim == 1 else a[:, 0]


def plot_sandpile_1d(
    scenario: SandpileScenario,
    ax: Axes | None = None,
    y_sand: float = 0.9,
    y_dest: float = -0.9,
    xpad: float = 0.6,
    show_labels: bool = True,
) -> Axes:
    """1 次元数直線上に砂山 (青丸, 上段) と行き先 (赤四角, 下段) を配置する.

    seminar 行 44–67 の TikZ 図に相当.

    Parameters
    ----------
    scenario : SandpileScenario
        1 次元の場合に限る. 2 次元以上は :func:`plot_assignment_2d` を参照.
    y_sand, y_dest : float
        砂山 / 行き先を描くラインの y 座標.
    xpad : float
        数直線の左右のマージン.
    """
    if scenario.x.ndim > 1 and scenario.x.shape[1] != 1:
        raise ValueError("plot_sandpile_1d は 1 次元シナリオ専用")
    if ax is None:
        _, ax = plt.subplots(figsize=(6.0, 3.0))

    xs = _x_flat(scenario.x)
    ys = _x_flat(scenario.y)
    x_min = float(min(xs.min(), ys.min()) - xpad)
    x_max = float(max(xs.max(), ys.max()) + xpad)

    # 数直線
    ax.axhline(0.0, color="gray", linewidth=1.0, alpha=0.6)
    for pos in np.arange(np.floor(x_min), np.ceil(x_max) + 1):
        ax.plot([pos, pos], [-0.07, 0.07], color="gray", linewidth=0.8, alpha=0.5)
        ax.text(pos, -0.22, f"{int(pos)}", ha="center", va="top", fontsize=8, color="gray")

    # 砂山 (青丸) — 質量をマーカーサイズに反映
    ax.scatter(
        xs,
        np.full_like(xs, y_sand),
        s=300 * scenario.a / scenario.a.max(),
        c="tab:blue",
        edgecolors="black",
        zorder=3,
        label="砂山 $x_i$",
    )
    # 行き先 (赤四角)
    ax.scatter(
        ys,
        np.full_like(ys, y_dest),
        s=300 * scenario.b / scenario.b.max(),
        c="tab:red",
        marker="s",
        edgecolors="black",
        zorder=3,
        label="行き先 $y_j$",
    )

    if show_labels:
        for i, xi in enumerate(xs):
            ax.annotate(
                f"$x_{{{i + 1}}}$",
                (xi, y_sand),
                textcoords="offset points",
                xytext=(0, 12),
                ha="center",
                fontsize=10,
                color="tab:blue",
            )
        for j, yj in enumerate(ys):
            ax.annotate(
                f"$y_{{{j + 1}}}$",
                (yj, y_dest),
                textcoords="offset points",
                xytext=(0, -14),
                ha="center",
                fontsize=10,
                color="tab:red",
            )
        # 砂山から数直線への点線と位置表示
        for xi in xs:
            ax.plot([xi, xi], [0, y_sand - 0.15], color="gray", linestyle=":", alpha=0.4)
        for yj in ys:
            ax.plot([yj, yj], [0, y_dest + 0.15], color="gray", linestyle=":", alpha=0.4)

    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_dest - 0.6, y_sand + 0.6)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    return ax


def plot_monge_map_1d(
    scenario: SandpileScenario,
    T_idx: MongeMap,
    ax: Axes | None = None,
    arrow_color: str = "tab:green",
) -> Axes:
    """1D 砂山配置図に Monge 写像 :math:`T(x_i) = y_{T_{\\mathrm{idx}}(i)}` を矢印で描く."""
    ax = plot_sandpile_1d(scenario, ax=ax)
    xs = _x_flat(scenario.x)
    ys = _x_flat(scenario.y)
    for i, j in enumerate(T_idx):
        ax.annotate(
            "",
            xy=(ys[int(j)], -0.75),
            xytext=(xs[i], 0.75),
            arrowprops={
                "arrowstyle": "->",
                "color": arrow_color,
                "linewidth": 2.0,
                "shrinkA": 6,
                "shrinkB": 6,
            },
        )
    return ax


def plot_assignment_1d(
    scenario: SandpileScenario,
    sigma: Permutation,
    ax: Axes | None = None,
    arrow_color: str = "tab:green",
) -> Axes:
    """1D 砂山配置図に割当 :math:`\\sigma` を矢印で描く.

    `sigma` は ``sigma[i] = j`` で 0-indexed. Monge 写像の特殊ケース.
    """
    return plot_monge_map_1d(scenario, sigma, ax=ax, arrow_color=arrow_color)


def plot_coupling_1d(
    scenario: SandpileScenario,
    P: TransportPlan,
    ax: Axes | None = None,
    max_linewidth: float = 4.0,
    tol: float = 1e-9,
) -> Axes:
    """1D 砂山配置図に Kantorovich カップリング :math:`P_{ij}` を太さで描く."""
    ax = plot_sandpile_1d(scenario, ax=ax)
    xs = _x_flat(scenario.x)
    ys = _x_flat(scenario.y)
    P_max = float(P.max())
    for i in range(P.shape[0]):
        for j in range(P.shape[1]):
            if P[i, j] <= tol:
                continue
            lw = max_linewidth * (P[i, j] / P_max)
            ax.annotate(
                "",
                xy=(ys[j], -0.75),
                xytext=(xs[i], 0.75),
                arrowprops={
                    "arrowstyle": "->",
                    "color": "tab:purple",
                    "linewidth": lw,
                    "alpha": 0.85,
                    "shrinkA": 6,
                    "shrinkB": 6,
                },
            )
            ax.text(
                0.5 * (xs[i] + ys[j]),
                0.0,
                f"{P[i, j]:.3g}",
                ha="center",
                va="center",
                fontsize=8,
                color="tab:purple",
                bbox={
                    "boxstyle": "round,pad=0.15",
                    "facecolor": "white",
                    "edgecolor": "tab:purple",
                    "alpha": 0.85,
                },
            )
    return ax


def plot_transport_plan_matrix(
    P: TransportPlan,
    ax: Axes | None = None,
    cmap: str = "Purples",
    annotate: bool = True,
) -> Axes:
    """輸送計画 :math:`\\mathbf{P}` のヒートマップ."""
    if ax is None:
        _, ax = plt.subplots(figsize=(4.2, 3.8))
    n, m = P.shape
    im = ax.imshow(P, cmap=cmap, origin="upper", vmin=0.0)
    ax.set_xticks(range(m), labels=[str(j + 1) for j in range(m)])
    ax.set_yticks(range(n), labels=[str(i + 1) for i in range(n)])
    ax.set_xlabel("行き先 $j$")
    ax.set_ylabel("砂山 $i$")
    if annotate:
        vmax = float(max(P.max(), 1e-12))
        for i in range(n):
            for j in range(m):
                val = P[i, j]
                color = "white" if val > vmax * 0.55 else "black"
                ax.text(j, i, f"{val:.3g}", ha="center", va="center", color=color, fontsize=9)
    ax.figure.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    return ax
