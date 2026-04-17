"""全列挙法とハンガリアン法の結果一致を数値的に確認する.

n = 3…7 のランダムコスト行列をそれぞれ複数生成し, 両手法の最適コストを比較する.
(seminar §sem-assignment 行 128–132 で言及される O(n³) アルゴリズムが
全列挙と同一の最適値を返すことを実測する.)
"""

from __future__ import annotations

import pathlib

import matplotlib.pyplot as plt
import numpy as np

from cot.assignment import AssignmentProblem, solve_brute_force, solve_hungarian
from cot.viz import use_japanese_font


def main() -> None:
    use_japanese_font()

    rng = np.random.default_rng(seed=20260417)
    ns = list(range(3, 8))
    trials_per_n = 30

    print("=" * 60)
    print("全列挙法 vs ハンガリアン法: 最適コストの差")
    print("=" * 60)

    diffs: list[tuple[int, float]] = []
    for n in ns:
        for _ in range(trials_per_n):
            C = rng.uniform(0.0, 10.0, size=(n, n))
            problem = AssignmentProblem(C)
            bf = solve_brute_force(problem)
            hu = solve_hungarian(problem)
            diffs.append((n, hu.cost - bf.cost))
        per_n = [d for m, d in diffs if m == n]
        max_abs = max(abs(d) for d in per_n)
        print(f"  n = {n}: {trials_per_n} 試行, max |diff| = {max_abs:.2e}")

    # --- 図: n ごとの差分の分布 (ほぼ 0 に集中することを可視化) ---
    fig, ax = plt.subplots(figsize=(7.0, 4.0))
    for n in ns:
        per_n = [d for m, d in diffs if m == n]
        ax.scatter([n] * len(per_n), per_n, alpha=0.6, label=f"n = {n}")
    ax.axhline(0, color="black", linewidth=0.8)
    ax.set_xlabel("$n$")
    ax.set_ylabel("ハンガリアン法コスト $-$ 全列挙コスト")
    ax.set_title(f"両手法は全 {len(diffs)} 試行で数値的に一致 (差は浮動小数点誤差のみ)")
    ax.grid(True, alpha=0.3)

    out = pathlib.Path(__file__).parent / "figures"
    out.mkdir(exist_ok=True)
    path = out / "03_hungarian_vs_brute.pdf"
    fig.tight_layout()
    fig.savefig(path)
    fig.savefig(path.with_suffix(".png"), dpi=150)
    print(f"\nsaved: {path}")


if __name__ == "__main__":
    main()
