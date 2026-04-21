"""seminar §sem-assignment (ch02_ot_foundations.tex 行 27–98) の n=2 例を再現する.

砂山 :math:`x = (0, 3)` と行き先 :math:`y = (1, 4)` の 1 次元配置に対し,
:math:`C_{ij} = |x_i - y_j|` で与えられる

.. math::
   C = \\begin{pmatrix} 1 & 4 \\\\ 2 & 1 \\end{pmatrix}

の下で, 2! = 2 通りの置換 :math:`\\sigma \\in \\mathrm{Perm}(2)` を全列挙し
最適 :math:`\\sigma^\\star = (1, 2)`, コスト :math:`1` を確認する.

標準出力に seminar 行 89–95 の表を再現し, ``figures/01_assignment.pdf`` に
  (左) コスト行列ヒートマップ
  (中) 2 通りの全列挙コスト棒グラフ
  (右) 1 次元配置図と最適 :math:`\\sigma^\\star` の矢印
の 3 パネル図を保存する.
"""

from __future__ import annotations

import pathlib

import matplotlib.pyplot as plt

from cot.assignment import AssignmentProblem, solve_brute_force
from cot.assignment.brute_force import enumerate_all
from cot.core.scenario import seminar_n2_scenario
from cot.viz import (
    plot_assignment_1d,
    plot_cost_matrix,
    plot_enumeration_bar,
    use_japanese_font,
)


def main() -> None:
    use_japanese_font()

    scenario = seminar_n2_scenario()
    problem = AssignmentProblem.from_scenario(scenario, p=1.0)

    solutions = list(enumerate_all(problem))
    optimal = solve_brute_force(problem)
    optimal_index = next(
        i
        for i, s in enumerate(solutions)
        if tuple(s.sigma.tolist()) == tuple(optimal.sigma.tolist())
    )

    # --- 標準出力: seminar 行 89–95 の表を再現 ---
    print("=" * 60)
    print("seminar §sem-assignment: 砂山 → 行き先 (n=2) 全列挙")
    print("=" * 60)
    print(f"砂山   x = {scenario.x.tolist()},  質量 a = {scenario.a.tolist()}")
    print(f"行き先 y = {scenario.y.tolist()},  質量 b = {scenario.b.tolist()}")
    print(f"\nC =\n{problem.C}\n")
    header = f"  {'σ (1-indexed)':<16}{'コスト (1/n Σ C_{i,σ(i)})':>28}"
    print(header)
    print("-" * len(header))
    for i, s in enumerate(solutions):
        mark = "  ← 最適" if i == optimal_index else ""
        print(f"  {str(s.sigma_one_indexed()):<16}{s.cost:>28.6f}{mark}")
    print("-" * len(header))
    print(f"最適 σ = {optimal.sigma_one_indexed()}, cost = {optimal.cost}")

    # --- 図: ヒートマップ + 棒グラフ + 1D 配置 ---
    fig, axes = plt.subplots(1, 3, figsize=(13.0, 4.0))
    plot_cost_matrix(problem.C, sigma=optimal.sigma, ax=axes[0])
    axes[0].set_title(r"コスト行列 $C$ と最適 $\sigma^\star$ (赤枠)")
    plot_enumeration_bar(solutions, optimal_index=optimal_index, ax=axes[1])
    axes[1].set_title("2 通りの置換と正規化コスト (緑 = 最適)")
    plot_assignment_1d(scenario, optimal.sigma, ax=axes[2])
    axes[2].set_title(rf"1D 配置と最適割当 $\sigma^\star = {optimal.sigma_one_indexed()}$")

    fig.tight_layout()
    out = pathlib.Path(__file__).parent / "figures"
    out.mkdir(exist_ok=True)
    path = out / "01_assignment.pdf"
    fig.savefig(path)
    fig.savefig(path.with_suffix(".png"), dpi=150)
    print(f"\nsaved: {path}")


if __name__ == "__main__":
    main()
