"""同じ砂山シナリオ (seminar §sem-assignment-cost-example) に対し,
最適割当 / Monge / Kantorovich の 3 問題を解き, 最適コストが一致することを確認する.

seminar の論理展開:
  * §sem-assignment  (ch02 行 7–132)   : 最適割当問題
  * §sem-monge       (ch02 行 136–419) : Monge 問題 (n=m, 均等質量で割当に還元)
  * §sem-kantorovich (ch02 行 424–563) : Kantorovich 緩和 (LP)

の「3 問題が同じ最適値を与える」ことを n=2 砂山例で数値的に示す.

``figures/04_three_problems.pdf`` に 3 パネルを横並びで保存する
  (左) 割当: σ* の矢印
  (中) Monge: 写像 T* の矢印 (割当と一致)
  (右) Kantorovich: カップリング P* の太さ付き矢印
"""

from __future__ import annotations

import pathlib

import matplotlib.pyplot as plt
import numpy as np

from cot.assignment import AssignmentProblem, solve_hungarian
from cot.core.scenario import seminar_n2_scenario
from cot.kantorovich import KantorovichProblem, solve_linprog
from cot.monge import MongeProblem
from cot.monge import solve_brute_force as monge_brute
from cot.viz import (
    plot_assignment_1d,
    plot_coupling_1d,
    plot_monge_map_1d,
    use_japanese_font,
)


def main() -> None:
    use_japanese_font()

    scenario = seminar_n2_scenario()

    # --- 3 問題をそれぞれ解く ---
    # 注意: 均等質量 a_i = 1/n において
    #   Assignment.cost = (1/n) Σ C_{i, σ(i)}
    #   Monge.cost      = Σ a_i · C_{i, T(i)}        = (1/n) Σ C_{i, T(i)}
    #   Kantorovich.cost = ⟨C, P⟩                      = (1/n) Σ C_{i, σ(i)}  (P = (1/n) Π_σ)
    # の 3 つはすべて同じスケールになる.
    ap = AssignmentProblem.from_scenario(scenario, p=1.0)
    a_sol = solve_hungarian(ap)

    mp = MongeProblem(scenario)
    m_sol = monge_brute(mp)

    kp = KantorovichProblem.from_scenario(scenario, p=1.0)
    k_sol = solve_linprog(kp)

    # --- 標準出力: 3 問題の比較表 ---
    print("=" * 60)
    print("3 問題の比較 (seminar §sem-assignment 例, n=2, 均等質量)")
    print("=" * 60)
    print(f"C = \n{kp.C}\n")
    rows = [
        (
            "Assignment",
            f"σ = {a_sol.sigma_one_indexed()}",
            "(1/n) Σ C_{i,σ(i)}",
            a_sol.cost,
        ),
        (
            "Monge (離散)",
            f"T = {m_sol.t_one_indexed()}",
            "Σ a_i · C_{i,T(i)}",
            m_sol.cost,
        ),
        (
            "Kantorovich",
            f"P = {np.round(k_sol.P, 3).tolist()}",
            "⟨C, P⟩",
            k_sol.cost,
        ),
    ]
    header = f"  {'問題':<14}{'解':<30}{'目的関数':<24}{'値':>10}"
    print(header)
    print("-" * len(header))
    for name, sol_str, obj_str, cost_val in rows:
        print(f"  {name:<14}{sol_str:<30}{obj_str:<24}{cost_val:>10.4f}")
    print("-" * len(header))

    costs = [a_sol.cost, m_sol.cost, k_sol.cost]
    all_match = np.allclose(costs, costs[0])
    print(f"\n3 問題すべて cost = {costs[0]} で一致: {all_match}")
    print(
        "→ n=m かつ a=b=(1/n)1 の balanced uniform では, "
        "Assignment = Monge = Kantorovich 端点 (置換行列)."
    )

    # --- 図: 3 パネル ---
    fig, axes = plt.subplots(1, 3, figsize=(13.5, 3.8))

    plot_assignment_1d(scenario, a_sol.sigma, ax=axes[0])
    axes[0].set_title(
        rf"(a) Assignment: $\sigma^\star = {a_sol.sigma_one_indexed()}$,  コスト $= {a_sol.cost}$"
    )

    plot_monge_map_1d(scenario, m_sol.T_idx, ax=axes[1], arrow_color="tab:blue")
    axes[1].set_title(rf"(b) Monge: $T^\star = {m_sol.t_one_indexed()}$,  コスト $= {m_sol.cost}$")

    plot_coupling_1d(scenario, k_sol.P, ax=axes[2])
    axes[2].set_title(rf"(c) Kantorovich: $\langle C, P^\star\rangle = {k_sol.cost}$")

    fig.tight_layout()
    out = pathlib.Path(__file__).parent / "figures"
    out.mkdir(exist_ok=True)
    path = out / "04_three_problems.pdf"
    fig.savefig(path)
    fig.savefig(path.with_suffix(".png"), dpi=150)
    print(f"\nsaved: {path}")


if __name__ == "__main__":
    main()
