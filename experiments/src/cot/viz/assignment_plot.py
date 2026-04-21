"""最適割当の可視化.

seminar の TikZ 図 (`seminar/ch02_ot_foundations.tex` 行 45–110 など) に対応する
matplotlib 版の描画関数を提供する.
"""

from __future__ import annotations

from collections.abc import Sequence

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes

from cot.assignment.definitions import AssignmentSolution
from cot.core.types import CostMatrix, Permutation


def plot_cost_matrix(
    C: CostMatrix,
    sigma: Permutation | None = None,
    ax: Axes | None = None,
    cmap: str = "viridis",
    annotate: bool = True,
) -> Axes:
    """コスト行列のヒートマップを描き, 選択された割当をマーカーで強調表示する.

    Parameters
    ----------
    C : shape ``(n, n)``
        コスト行列.
    sigma : shape ``(n,)``, optional
        強調したい置換 (0-indexed). ``None`` なら強調なし.
    ax : matplotlib Axes, optional
        描画先. ``None`` なら新規作成.
    cmap : str
        カラーマップ名.
    annotate : bool
        各セルにコスト値をテキスト表示するか.
    """
    if ax is None:
        _, ax = plt.subplots(figsize=(4.5, 4.0))
    n = C.shape[0]
    im = ax.imshow(C, cmap=cmap, origin="upper")
    ax.set_xticks(range(n), labels=[str(j + 1) for j in range(n)])
    ax.set_yticks(range(n), labels=[str(i + 1) for i in range(n)])
    ax.set_xlabel("行き先 $j$")
    ax.set_ylabel("砂山 $i$")
    if annotate:
        vmax = float(np.max(C))
        for i in range(n):
            for j in range(n):
                color = "white" if C[i, j] < vmax * 0.55 else "black"
                ax.text(j, i, f"{C[i, j]:.3g}", ha="center", va="center", color=color, fontsize=9)
    if sigma is not None:
        for i, j in enumerate(sigma):
            ax.add_patch(
                plt.Rectangle(
                    (j - 0.5, i - 0.5),
                    1,
                    1,
                    fill=False,
                    edgecolor="red",
                    linewidth=2.5,
                )
            )
    ax.figure.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    return ax


def plot_assignment_2d(
    X: np.ndarray,
    Y: np.ndarray,
    sigma: Permutation | Sequence[int],
    ax: Axes | None = None,
    title: str | None = None,
    color: str = "C0",
    linestyle: str = "-",
    draw_points: bool = True,
    show_legend: bool = True,
) -> Axes:
    """2 次元配置図: 砂山 :math:`x_i` (青丸) と行き先 :math:`y_j` (赤四角)
    を散布し, 割当 :math:`\\sigma` に沿って矢印を描く.

    Parameters
    ----------
    X : shape ``(n, 2)``
        砂山の 2D 座標.
    Y : shape ``(n, 2)``
        行き先の 2D 座標.
    sigma : shape ``(n,)``
        描画する割当 (0-indexed).
    draw_points : bool
        砂山・行き先のマーカーを描画するか. 複数の割当を重ね描きする際は
        2 回目以降で ``False`` を渡すとマーカーの二重描画を避けられる.
    show_legend : bool
        凡例を表示するか.
    """
    if ax is None:
        _, ax = plt.subplots(figsize=(4.5, 4.5))
    X = np.asarray(X, dtype=np.float64)
    Y = np.asarray(Y, dtype=np.float64)
    if draw_points:
        ax.scatter(
            X[:, 0],
            X[:, 1],
            s=140,
            c="tab:blue",
            marker="o",
            edgecolors="black",
            label="砂山 $x_i$",
            zorder=3,
        )
        ax.scatter(
            Y[:, 0],
            Y[:, 1],
            s=140,
            c="tab:red",
            marker="s",
            edgecolors="black",
            label="行き先 $y_j$",
            zorder=3,
        )
        for i, xi in enumerate(X):
            ax.annotate(
                f"$x_{{{i + 1}}}$", xi, textcoords="offset points", xytext=(8, 8), fontsize=10
            )
        for j, yj in enumerate(Y):
            ax.annotate(
                f"$y_{{{j + 1}}}$", yj, textcoords="offset points", xytext=(8, 8), fontsize=10
            )
    for i, j in enumerate(sigma):
        ax.annotate(
            "",
            xy=Y[j],
            xytext=X[i],
            arrowprops={
                "arrowstyle": "->",
                "color": color,
                "linestyle": linestyle,
                "linewidth": 1.8,
                "shrinkA": 10,
                "shrinkB": 10,
            },
        )
    ax.set_aspect("equal", adjustable="box")
    if title is not None:
        ax.set_title(title)
    if show_legend and draw_points:
        ax.legend(loc="best", fontsize=9)
    ax.grid(True, alpha=0.3)
    return ax


def plot_enumeration_bar(
    solutions: Sequence[AssignmentSolution],
    optimal_index: int | None = None,
    ax: Axes | None = None,
) -> Axes:
    """全列挙した割当のコストを棒グラフで並列表示.

    seminar の ``§sem-assignment`` 例 (6 通りのコスト表) を可視化.
    """
    if ax is None:
        _, ax = plt.subplots(figsize=(6.0, 3.5))
    costs = [s.cost for s in solutions]
    labels = [str(s.sigma_one_indexed()) for s in solutions]
    colors = ["tab:gray"] * len(solutions)
    if optimal_index is not None:
        colors[optimal_index] = "tab:green"
    ax.bar(range(len(solutions)), costs, color=colors, edgecolor="black")
    ax.set_xticks(range(len(solutions)), labels=labels, rotation=0, fontsize=9)
    ax.set_xlabel(r"$\sigma$")
    ax.set_ylabel(r"$\frac{1}{n}\sum_i C_{i,\sigma(i)}$")
    ax.grid(True, axis="y", alpha=0.3)
    return ax
