# cot — Computational Optimal Transport

リポジトリ `computational-optimal-transport` のセミナー原稿 (`../seminar/`) の内容を
Python で実装し, 数値的に確認するためのパッケージ.
Cuturi–Peyré の論文 ([arXiv:1803.00567](https://arxiv.org/abs/1803.00567)) の
記法 (preamble.tex) に合わせて実装している.

## 現在の実装範囲

| 節 (seminar) | 実装箇所 | 内容 |
|---|---|---|
| `§sem-assignment` (`ch02_ot_foundations.tex:7–132`) | `cot.assignment` | 最適割当問題 (全列挙 / ハンガリアン法) |
| `§sem-monge` (`ch02_ot_foundations.tex:136–419`) | `cot.monge` | 離散 Monge 問題 (全写像列挙 + 押出可能性検査) |
| `§sem-kantorovich` (`ch02_ot_foundations.tex:424–563`) | `cot.kantorovich` | 離散 Kantorovich 問題 (LP, `scipy.optimize.linprog`) |

題材はすべて **砂山 → 行き先** で統一. 共通シナリオは
`cot.core.seminar_n2_scenario()` (seminar §sem-assignment-cost-example の n=2 例).

将来拡張予定: Wasserstein 距離, Sinkhorn アルゴリズム, エントロピー正則化.

## パッケージ構成

```
src/cot/
├── core/
│   ├── scenario     # SandpileScenario / seminar_n2_scenario
│   ├── costs        # pairwise_distance_matrix
│   └── types        # 型エイリアス (CostMatrix, Permutation, TransportPlan, MongeMap)
├── assignment/      # 最適割当問題 (§sem-assignment)
│   ├── definitions  # AssignmentProblem / AssignmentSolution
│   ├── brute_force  # n! 全列挙 (solve_brute_force, enumerate_all)
│   └── hungarian    # scipy ラッパ (solve_hungarian)
├── monge/           # 離散 Monge 問題 (§sem-monge)
│   ├── definitions  # MongeProblem / MongeSolution
│   └── brute_force  # m^n 全写像列挙+押出フィルタ (solve_brute_force, enumerate_feasible)
├── kantorovich/     # 離散 Kantorovich 問題 (§sem-kantorovich)
│   ├── definitions  # KantorovichProblem / KantorovichSolution
│   └── linprog      # scipy.optimize.linprog による LP 解法 (solve_linprog)
└── viz/             # matplotlib 可視化 (optional-deps "viz")
    ├── assignment_plot  # ヒートマップ・2D 配置・棒グラフ
    └── sandpile_plot    # 1D 配置・輸送計画ヒートマップ・カップリング矢印
```

## Quick start

[uv](https://docs.astral.sh/uv/) があれば依存は自動で揃う.

```bash
uv run python examples/01_assignment.py         # §sem-assignment n=2 例の再現
uv run python examples/02_monge.py              # §sem-monge 離散写像の全列挙と押出検査
uv run python examples/03_kantorovich.py        # §sem-kantorovich LP による輸送計画
uv run python examples/04_three_problems.py     # 3 問題を同一シナリオで比較
uv run python examples/05_assignment_nonunique.py  # 命題 sem-uniqueness (2D)
uv run python examples/06_hungarian_vs_brute.py    # 数値的一致の確認
uv run python examples/07_benchmark_complexity.py  # n! vs O(n³) のベンチマーク
```

各スクリプトは stdout に結果表を出し, `examples/figures/` に PDF と PNG を保存する.

Python から直接:

```python
import numpy as np
from cot.core import seminar_n2_scenario
from cot.assignment import AssignmentProblem, solve_hungarian
from cot.monge import MongeProblem, solve_brute_force as monge_solve
from cot.kantorovich import KantorovichProblem, solve_linprog

scenario = seminar_n2_scenario()   # 砂山 x=[0,3], 行き先 y=[1,4], a=b=(1/2,1/2)

# 最適割当
a_sol = solve_hungarian(AssignmentProblem.from_scenario(scenario, p=1.0))
print(a_sol.sigma_one_indexed(), a_sol.cost)    # → (1, 2)  1.0

# 離散 Monge
m_sol = monge_solve(MongeProblem(scenario))
print(m_sol.T_one_indexed(), m_sol.cost)         # → (1, 2)  1.0

# 離散 Kantorovich
k_sol = solve_linprog(KantorovichProblem.from_scenario(scenario, p=1.0))
print(k_sol.P, k_sol.cost)
# → [[0.5, 0. ], [0. , 0.5]]  1.0
```

3 問題いずれもコスト 1.0 に一致 (seminar 行 201–213 の「Monge→割当の還元」と,
balanced uniform 下の Kantorovich 最適端点が置換行列になる性質による).

## lint / format

```bash
uv run ruff check src examples
uv run ruff format src examples
```

## 記法対応

| 数学記法 (preamble.tex) | Python | 備考 |
|---|---|---|
| $C \in \mathbb{R}_+^{n\times m}$ | `C: np.ndarray` | コスト行列 |
| $\sigma \in \mathrm{Perm}(n)$ | `sigma: np.ndarray[int]` | **0-indexed** で保持. `sigma_one_indexed()` で 1-indexed タプルに変換 |
| $T\colon \X \to \Y$ (離散) | `T_idx: np.ndarray[int]` | `T_idx[i] = j` ⇔ $T(x_i) = y_j$ |
| $\mathbf{P} \in \mathrm{CouplingsD}(\mathbf{a}, \mathbf{b})$ | `P: np.ndarray` | 離散カップリング (輸送計画) |
| $\langle \mathbf{C}, \mathbf{P}\rangle$ | `np.sum(C * P)` | Frobenius 内積 |
| $\frac{1}{n}\sum_i C_{i,\sigma(i)}$ | `AssignmentSolution.cost` | seminar の正規化コスト |

## 拡張ガイドライン

- 新規サブパッケージは「seminar または `../chapters/` に対応節がある」ことを条件とする.
- production 依存は現状 `numpy`, `scipy` のみ. これを超える追加は MVP 逸脱を疑う.
