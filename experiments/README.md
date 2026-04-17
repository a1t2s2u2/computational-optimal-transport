# cot — Computational Optimal Transport

リポジトリ `computational-optimal-transport` のセミナー原稿 (`../seminar/`) の内容を
Python で実装し, 数値的に確認するためのパッケージ.
Cuturi–Peyré の論文 ([arXiv:1803.00567](https://arxiv.org/abs/1803.00567)) の
記法 (preamble.tex) に合わせて実装している.

## 現在の実装範囲 (MVP)

| 節 (seminar) | 実装箇所 | 内容 |
|---|---|---|
| `§sem-assignment` (`ch02_ot_foundations.tex:7–171`) | `cot.assignment` | 最適割当問題 (全列挙 / ハンガリアン法) |

将来拡張予定: Monge 問題, Kantorovich 問題, Wasserstein 距離, Sinkhorn アルゴリズム.

## インストール

[uv](https://docs.astral.sh/uv/) (>= 0.4) が必要.

```bash
cd experiments
uv sync --all-extras --group dev
```

Python 3.11 以降が自動で用意される.

## パッケージ構成

```
src/cot/
├── core/             # 共通: 型, コスト行列, ヒストグラム
├── assignment/       # 最適割当問題 (§sem-assignment)
│   ├── definitions   # AssignmentProblem / AssignmentSolution
│   ├── brute_force   # n! 全列挙 (solve_brute_force, enumerate_all)
│   └── hungarian     # scipy ラッパ (solve_hungarian)
└── viz/              # matplotlib 可視化 (optional-deps "viz")
```

## Quick start

```python
import numpy as np
from cot.assignment import AssignmentProblem, solve_brute_force, solve_hungarian

# seminar §sem-assignment の 3×3 例
C = np.array([[5, 2, 8],
              [7, 4, 1],
              [3, 9, 6]], dtype=float)

problem = AssignmentProblem(C)
solution = solve_hungarian(problem)

print(solution.sigma_one_indexed())   # → (2, 3, 1)
print(solution.cost)                  # → 2.0 (= (2+1+3)/3)
print(solution.P)                     # 置換行列 (要素 1/n)
```

`AssignmentSolution.cost` は seminar 定義 (`ch02_ot_foundations.tex:17–22`) の
正規化コスト $\frac{1}{n}\sum_i C_{i,\sigma(i)}$.
`scipy.optimize.linear_sum_assignment` が返す生の和との違いに注意.

## examples の実行

各スクリプトは単独で実行可能で, `examples/figures/` に PDF と PNG を保存する.

```bash
uv run python examples/01_assignment_3x3.py       # §sem-assignment 3×3 の再現
uv run python examples/02_assignment_nonunique.py # remark sem-uniqueness
uv run python examples/03_hungarian_vs_brute.py   # 数値的一致の確認
uv run python examples/04_benchmark_complexity.py # n! vs O(n³) のベンチマーク
```

## lint / format

```bash
uv run ruff check src tests examples
uv run ruff format src tests examples
```

## 記法対応

| 数学記法 (preamble.tex) | Python | 備考 |
|---|---|---|
| $C \in \mathbb{R}^{n\times n}$ | `C: np.ndarray` | コスト行列 |
| $\sigma \in \mathrm{Perm}(n)$ | `sigma: np.ndarray[int]` | **0-indexed** で保持. `sigma_one_indexed()` で 1-indexed タプルに変換 |
| $P_\sigma$ (置換行列, 要素 $1/n$) | `solution.P` | seminar 定義 (`ch02_ot_foundations.tex:17–31`) |
| $\frac{1}{n}\sum_i C_{i,\sigma(i)}$ | `solution.cost` | seminar の正規化コスト |
| $\mathbf{a} \in \Sigma_n$ | `cot.core.histograms.uniform(n)` | 一様測度 |

## 拡張ガイドライン

- 新規サブパッケージは「seminar または `../chapters/` の `04_entropic_regularization.tex` など
  に対応節がある」ことを条件とする.
- production 依存は現状 `numpy`, `scipy` のみ. これを超える追加は MVP 逸脱を疑う.
