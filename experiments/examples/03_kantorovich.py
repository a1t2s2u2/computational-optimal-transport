"""seminar §sem-kantorovich (ch02_ot_foundations.tex 行 424–563) の離散 Kantorovich 問題.

砂山 :math:`\\mathbf{a} = (1/2, 1/2)` から行き先 :math:`\\mathbf{b} = (1/2, 1/2)` への
輸送計画 :math:`\\mathbf{P} \\in \\mathrm{CouplingsD}(\\mathbf{a}, \\mathbf{b})` の
うち, Frobenius 内積 :math:`\\langle \\mathbf{C}, \\mathbf{P} \\rangle` を最小化する
線形計画問題:

.. math::
   \\min_{\\mathbf{P} \\geq 0}\\; \\langle \\mathbf{C}, \\mathbf{P} \\rangle
   \\quad \\text{s.t.} \\quad
   \\mathbf{P}\\mathbf{1}_m = \\mathbf{a},\\;
   \\mathbf{P}^\\top\\mathbf{1}_n = \\mathbf{b}.

``scipy.optimize.linprog`` (HiGHS) で解き, n=m=2 均等質量の場合は最適解が
``P* = diag(1/2, 1/2)``, コスト 1 になること — すなわち最適割当と一致すること — を
確認する.

``figures/03_kantorovich.pdf`` に
  (左) 輸送計画 P* のヒートマップ
  (中) 1 次元配置図と P* の太さ付き矢印
  (右) 許容カップリング多面体のパラメタ化 t ↦ P(t) に沿ったコスト関数
の 3 パネル図を保存する.
"""

from __future__ import annotations

import pathlib

import matplotlib.pyplot as plt
import numpy as np

from cot.core.scenario import seminar_n2_scenario
from cot.kantorovich import KantorovichProblem, solve_linprog
from cot.viz import (
    plot_coupling_1d,
    plot_transport_plan_matrix,
    use_japanese_font,
)


def main() -> None:
    use_japanese_font()

    scenario = seminar_n2_scenario()
    problem = KantorovichProblem.from_scenario(scenario, p=1.0)

    solution = solve_linprog(problem)

    print("=" * 60)
    print("seminar §sem-kantorovich: 離散 Kantorovich (n=m=2)")
    print("=" * 60)
    print(f"a = {problem.a.tolist()}")
    print(f"b = {problem.b.tolist()}")
    print(f"C =\n{problem.C}\n")
    print("最適輸送計画 P* =")
    print(solution.P)
    print(f"\nコスト ⟨C, P*⟩ = {solution.cost}")
    print("行周辺 P*·1_m =", solution.P.sum(axis=1).tolist(), "  (= a)")
    print("列周辺 P*ᵀ·1_n =", solution.P.sum(axis=0).tolist(), "  (= b)")

    # n=m=2, a=b=1/2 の場合, カップリング多面体は 1 自由度の線分
    # P(t) = [[t, 1/2-t], [1/2-t, t]], t ∈ [0, 1/2] ─ 両端点が 2 つの置換行列
    print(
        "\n許容カップリング多面体 (n=m=2, 均等質量) は 1 自由度の線分:\n"
        "  P(t) = [[t, 1/2-t], [1/2-t, t]],  t ∈ [0, 1/2]"
    )
    t_values = np.linspace(0.0, 0.5, 101)
    costs = [
        float(
            problem.C[0, 0] * t
            + problem.C[0, 1] * (0.5 - t)
            + problem.C[1, 0] * (0.5 - t)
            + problem.C[1, 1] * t
        )
        for t in t_values
    ]
    t_star = 0.5 if solution.P[0, 0] > 0.25 else 0.0
    print(f"  t* = {t_star} (最適端点)")

    # --- 図: (左) P ヒートマップ, (中) 1D 配置+P 矢印, (右) 多面体上のコスト ---
    fig, axes = plt.subplots(1, 3, figsize=(13.5, 4.0))

    plot_transport_plan_matrix(solution.P, ax=axes[0])
    axes[0].set_title(r"最適輸送計画 $P^\star$ (Frobenius $\langle C, P\rangle = 1$)")

    plot_coupling_1d(scenario, solution.P, ax=axes[1])
    axes[1].set_title(r"1D 配置と $P^\star$ (矢印の太さ $\propto P_{ij}$)")

    ax = axes[2]
    ax.plot(t_values, costs, color="tab:purple", linewidth=2.0)
    ax.scatter(
        [0.0, 0.5],
        [costs[0], costs[-1]],
        c=["tab:orange", "tab:green"],
        s=80,
        zorder=3,
        label=r"端点 (置換行列)",
    )
    ax.scatter(
        [t_star], [solution.cost], c="tab:green", s=160, marker="*", zorder=4, label=r"最適 $t^\star$"
    )
    ax.axhline(solution.cost, color="tab:green", linestyle="--", alpha=0.5)
    ax.set_xlabel(r"$t \in [0, 1/2]$  (多面体を貫くパラメタ)")
    ax.set_ylabel(r"$\langle C, P(t) \rangle$")
    ax.set_title(r"$P(t)$ 上のコスト:  $P_{11} = P_{22} = t$,  $P_{12} = P_{21} = 1/2 - t$")
    ax.grid(True, alpha=0.3)
    ax.legend(loc="best", fontsize=9)

    fig.tight_layout()
    out = pathlib.Path(__file__).parent / "figures"
    out.mkdir(exist_ok=True)
    path = out / "03_kantorovich.pdf"
    fig.savefig(path)
    fig.savefig(path.with_suffix(".png"), dpi=150)
    print(f"\nsaved: {path}")


if __name__ == "__main__":
    main()
