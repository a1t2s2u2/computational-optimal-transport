"""seminar §sem-monge (ch02_ot_foundations.tex 行 139–213) の離散 Monge 問題を再現する.

砂山 :math:`\\alpha = \\tfrac{1}{2}\\delta_0 + \\tfrac{1}{2}\\delta_3` を
行き先 :math:`\\beta = \\tfrac{1}{2}\\delta_1 + \\tfrac{1}{2}\\delta_4` に押し出す
写像 :math:`T \\colon \\{x_1, x_2\\} \\to \\{y_1, y_2\\}` をすべて列挙
(2^2 = 4 通り) し, 押し出し条件 :math:`T\\pushforward\\alpha = \\beta` を満たすものの
うち総コスト最小のものを求める.

n = m, a = b = (1/n)1 なので全単射 (置換) だけが押し出し条件を通り, 最適割当問題に
帰着する (seminar 行 201–213). `01_assignment.py` と同じ解 σ = (1, 2), cost = 1
が得られる.

``figures/02_monge.pdf`` に
  (左) 全 4 写像の実行可能性とコスト表
  (右) 1 次元配置図と最適写像 T* の矢印
を保存する.
"""

from __future__ import annotations

import math
import pathlib
from itertools import product

import matplotlib.pyplot as plt
import numpy as np

from cot.core.scenario import seminar_n2_scenario
from cot.monge import MongeProblem, enumerate_feasible, solve_brute_force
from cot.viz import plot_monge_map_1d, use_japanese_font


def _pushforward(T_idx: np.ndarray, a: np.ndarray, m: int) -> np.ndarray:
    """離散押し出し :math:`\\sum_{i : T(i) = j} a_i` を計算する."""
    pushed = np.zeros(m, dtype=np.float64)
    for i, j in enumerate(T_idx):
        pushed[int(j)] += a[i]
    return pushed


def main() -> None:
    use_japanese_font()

    scenario = seminar_n2_scenario()
    problem = MongeProblem(scenario)

    # --- 全 m^n = 4 写像を列挙し, 実行可能性を検査 ---
    all_maps: list[tuple[tuple[int, ...], bool, float]] = []
    for T_tuple in product(range(problem.m), repeat=problem.n):
        T_idx = np.array(T_tuple, dtype=np.int64)
        pushed = _pushforward(T_idx, scenario.a, problem.m)
        feas = bool(np.allclose(pushed, scenario.b))
        cost = float(np.sum(scenario.a * problem.C[np.arange(problem.n), T_idx]))
        all_maps.append((tuple(int(j) + 1 for j in T_idx), feas, cost))

    feasible_sols = list(enumerate_feasible(problem))
    optimal = solve_brute_force(problem)

    # --- 標準出力 ---
    print("=" * 60)
    print("seminar §sem-monge: 砂山 → 行き先 (n=m=2, 均等質量)")
    print("=" * 60)
    print(f"α = {scenario.a.tolist()}·δ_x,  x = {scenario.x.tolist()}")
    print(f"β = {scenario.b.tolist()}·δ_y,  y = {scenario.y.tolist()}")
    print(f"\nC =\n{problem.C}\n")
    print("全 m^n = 4 写像とその状態:")
    header = f"  {'T (1-indexed)':<14}{'実行可能':^12}{'コスト':>14}"
    print(header)
    print("-" * len(header))
    for t, feas, cost in all_maps:
        mark = "✓" if feas else "×"
        cost_str = f"{cost:.3f}" if feas else "-"
        is_opt = feas and np.isclose(cost, optimal.cost)
        suffix = "  ← 最適" if is_opt else ""
        print(f"  {str(t):<14}{mark:^12}{cost_str:>14}{suffix}")
    print("-" * len(header))
    print(
        f"実行可能な写像: {len(feasible_sols)} 通り "
        f"(均等質量 n=m の場合は |Perm(n)|={math.factorial(problem.n)} に一致)"
    )
    print(f"最適 T = {optimal.T_one_indexed()}, cost = {optimal.cost}")
    print("\n→ Monge 問題 (均等質量 n=m) は最適割当問題と同じ解を返す (seminar 行 201–213).")

    # --- 図: (左) 実行可能性とコスト表, (右) 1D 配置図 ---
    fig, axes = plt.subplots(1, 2, figsize=(11.0, 4.2))

    ax = axes[0]
    ax.axis("off")
    row_labels = [str(t) for t, _, _ in all_maps]
    cell_text = []
    for t, feas, cost in all_maps:
        mark = "✓ 可" if feas else "× 不可"
        cost_str = f"{cost:.3f}" if feas else "—"
        cell_text.append([mark, cost_str])
    table = ax.table(
        cellText=cell_text,
        rowLabels=row_labels,
        colLabels=["押出可能", "コスト"],
        cellLoc="center",
        rowLoc="center",
        loc="center",
    )
    table.auto_set_font_size(False)
    table.set_fontsize(11)
    table.scale(1.0, 1.8)
    for i, (_, feas, cost) in enumerate(all_maps):
        color = "#e8f5e9" if feas and np.isclose(cost, optimal.cost) else "white"
        if feas and not np.isclose(cost, optimal.cost):
            color = "#fffde7"
        table[(i + 1, 0)].set_facecolor(color)
        table[(i + 1, 1)].set_facecolor(color)
    ax.set_title(r"全 $m^n = 4$ 写像: 押出条件と総コスト")

    plot_monge_map_1d(scenario, optimal.T_idx, ax=axes[1])
    axes[1].set_title(
        rf"最適 Monge 写像 $T^\star = {optimal.T_one_indexed()}$,  "
        rf"コスト $= {optimal.cost}$"
    )

    fig.tight_layout()
    out = pathlib.Path(__file__).parent / "figures"
    out.mkdir(exist_ok=True)
    path = out / "02_monge.pdf"
    fig.savefig(path)
    fig.savefig(path.with_suffix(".png"), dpi=150)
    print(f"\nsaved: {path}")


if __name__ == "__main__":
    main()
