"""seminar §sem-assignment の命題 sem-uniqueness (ch02 行 120–131) を 2D で例示する.

正方形の対角頂点に砂山と行き先を配置するとすべての距離が等しくなり,
2 通りの割当 σ = (1, 2) と σ = (2, 1) がともに最適となる.

    x_1 = (0, 0), x_2 = (1, 1)   (砂山, 青丸)
    y_1 = (1, 0), y_2 = (0, 1)   (行き先, 赤四角)
"""

from __future__ import annotations

import pathlib

import matplotlib.pyplot as plt
import numpy as np

from cot.assignment import AssignmentProblem
from cot.assignment.brute_force import enumerate_all
from cot.core.costs import pairwise_distance_matrix
from cot.viz import plot_assignment_2d, use_japanese_font


def main() -> None:
    use_japanese_font()

    X = np.array([[0.0, 0.0], [1.0, 1.0]])
    Y = np.array([[1.0, 0.0], [0.0, 1.0]])
    C = pairwise_distance_matrix(X, Y, p=1.0)
    problem = AssignmentProblem(C)

    solutions = list(enumerate_all(problem))
    min_cost = min(s.cost for s in solutions)
    optimals = [s for s in solutions if np.isclose(s.cost, min_cost)]

    print("=" * 56)
    print("seminar 命題 sem-uniqueness: n=2 非一意性 (2D)")
    print("=" * 56)
    print(f"砂山   x_1 = {X[0].tolist()}, x_2 = {X[1].tolist()}")
    print(f"行き先 y_1 = {Y[0].tolist()}, y_2 = {Y[1].tolist()}")
    print(f"\nC =\n{C}\n")
    print("全 2! = 2 通りの割当とコスト:")
    for s in solutions:
        print(f"  σ = {s.sigma_one_indexed()}, cost = {s.cost}")
    print(f"\n最適 σ は {len(optimals)} 通り存在, いずれも cost = {min_cost}")

    # --- 図: 2 つの最適割当を重ね描き ---
    fig, ax = plt.subplots(figsize=(5.2, 5.2))
    # 1 本目: 実線 (青) — マーカーと凡例もここで描画
    plot_assignment_2d(X, Y, optimals[0].sigma, ax=ax, color="tab:blue", linestyle="-")
    # 2 本目: 点線 (灰) — 矢印のみ重ね描き
    plot_assignment_2d(
        X,
        Y,
        optimals[1].sigma,
        ax=ax,
        color="gray",
        linestyle="--",
        draw_points=False,
        show_legend=False,
    )
    labels = [str(s.sigma_one_indexed()) for s in optimals]
    ax.set_title(f"2 つの最適割当: {labels[0]} (実線) と {labels[1]} (破線), ともに cost = 1")
    ax.set_xlim(-0.35, 1.35)
    ax.set_ylim(-0.35, 1.35)

    out = pathlib.Path(__file__).parent / "figures"
    out.mkdir(exist_ok=True)
    path = out / "05_assignment_nonunique.pdf"
    fig.tight_layout()
    fig.savefig(path)
    fig.savefig(path.with_suffix(".png"), dpi=150)
    print(f"\nsaved: {path}")


if __name__ == "__main__":
    main()
