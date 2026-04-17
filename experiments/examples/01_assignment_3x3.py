"""seminar §sem-assignment (行 24–126) の 3×3 例を再現する.

コスト行列
    C = [[5, 2, 8],
         [7, 4, 1],
         [3, 9, 6]]
に対し, 3! = 6 通りの置換を全列挙してコストを比較し,
最適 σ = (2, 3, 1), cost = 2 を確認する.

標準出力に seminar 行 115–123 の表を再現し,
``figures/01_assignment_3x3.pdf`` にコスト行列ヒートマップと
全列挙コスト棒グラフを保存する.
"""

from __future__ import annotations

import pathlib

import matplotlib.pyplot as plt
import numpy as np

from cot.assignment import AssignmentProblem, solve_brute_force
from cot.assignment.brute_force import enumerate_all
from cot.viz import plot_cost_matrix, plot_enumeration_bar, use_japanese_font


def main() -> None:
    use_japanese_font()

    C = np.array(
        [
            [5, 2, 8],
            [7, 4, 1],
            [3, 9, 6],
        ],
        dtype=float,
    )
    problem = AssignmentProblem(C)

    solutions = list(enumerate_all(problem))
    optimal = solve_brute_force(problem)
    optimal_index = next(
        i
        for i, s in enumerate(solutions)
        if tuple(s.sigma.tolist()) == tuple(optimal.sigma.tolist())
    )

    # --- 標準出力: seminar 行 115–123 の表を再現 ---
    print("=" * 56)
    print("seminar §sem-assignment: 3×3 全列挙")
    print("=" * 56)
    print(f"C =\n{C}\n")
    header = f"  {'σ (1-indexed)':<18}{'コスト (1/n Σ C_{i,σ(i)})':>24}"
    print(header)
    print("-" * len(header))
    for i, s in enumerate(solutions):
        mark = "  ← 最適" if i == optimal_index else ""
        print(f"  {str(s.sigma_one_indexed()):<18}{s.cost:>24.6f}{mark}")
    print("-" * len(header))
    print(f"最適 σ = {optimal.sigma_one_indexed()}, cost = {optimal.cost}")

    # --- 図: 左にヒートマップ, 右に全列挙棒グラフ ---
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.2))
    plot_cost_matrix(C, sigma=optimal.sigma, ax=axes[0])
    axes[0].set_title(r"コスト行列 $C$ と最適割当 $\sigma^\star$ (赤枠)")
    plot_enumeration_bar(solutions, optimal_index=optimal_index, ax=axes[1])
    axes[1].set_title("6 通りの置換と正規化コスト (緑 = 最適)")

    fig.tight_layout()
    out = pathlib.Path(__file__).parent / "figures"
    out.mkdir(exist_ok=True)
    path = out / "01_assignment_3x3.pdf"
    fig.savefig(path)
    fig.savefig(path.with_suffix(".png"), dpi=150)
    print(f"\nsaved: {path}")


if __name__ == "__main__":
    main()
