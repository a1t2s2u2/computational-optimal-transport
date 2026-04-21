"""全列挙法とハンガリアン法の計算時間を比較する.

砂山 → 行き先 の最適割当問題 (§sem-assignment) において,
seminar 行 100–103:
    「n! は急激に増大し, n = 70 でも n! > 10^100」
「ハンガリアン法やオークションアルゴリズムなど O(n³) で解ける手法が知られている」

本スクリプトは n = 3…最大値 までの実行時間を実測し, log-y プロットで
階乗的増加 vs 多項式増加の差を可視化する.
"""

from __future__ import annotations

import math
import pathlib
import time

import matplotlib.pyplot as plt
import numpy as np

from cot.assignment import AssignmentProblem, solve_brute_force, solve_hungarian
from cot.viz import use_japanese_font

BRUTE_MAX_N = 10  # brute force は n=10 (10! ≈ 3.6e6) までに制限
HUNGARIAN_MAX_N = 200


def measure(fn, problem: AssignmentProblem, repeats: int = 3) -> float:
    """``fn(problem)`` を ``repeats`` 回実行して最短時間 [秒] を返す."""
    best = math.inf
    for _ in range(repeats):
        t0 = time.perf_counter()
        fn(problem)
        dt = time.perf_counter() - t0
        best = min(best, dt)
    return best


def main() -> None:
    use_japanese_font()

    rng = np.random.default_rng(seed=20260417)

    brute_ns = list(range(3, BRUTE_MAX_N + 1))
    brute_times = []
    print("全列挙法 (brute force):")
    for n in brute_ns:
        C = rng.uniform(0.0, 10.0, size=(n, n))
        t = measure(solve_brute_force, AssignmentProblem(C), repeats=1 if n >= 9 else 3)
        brute_times.append(t)
        print(f"  n = {n:3d} (n! = {math.factorial(n):>10d}): {t:.4e} s")

    hungarian_ns = [3, 5, 10, 20, 50, 100, HUNGARIAN_MAX_N]
    hungarian_times = []
    print("\nハンガリアン法 (scipy.linear_sum_assignment):")
    for n in hungarian_ns:
        C = rng.uniform(0.0, 10.0, size=(n, n))
        t = measure(solve_hungarian, AssignmentProblem(C), repeats=5)
        hungarian_times.append(t)
        print(f"  n = {n:3d}: {t:.4e} s")

    # --- 図: log-y 軸で両者を重ね描き ---
    fig, ax = plt.subplots(figsize=(7.5, 4.5))
    ax.semilogy(brute_ns, brute_times, "o-", color="tab:red", label=r"全列挙 ($O(n!)$)")
    ax.semilogy(
        hungarian_ns, hungarian_times, "s-", color="tab:blue", label=r"ハンガリアン法 ($O(n^3)$)"
    )
    ax.set_xlabel("$n$")
    ax.set_ylabel("実行時間 [秒] (log スケール)")
    ax.set_title("最適割当の計算複雑性: 全列挙 vs ハンガリアン法")
    ax.grid(True, which="both", alpha=0.3)
    ax.legend(loc="best")

    out = pathlib.Path(__file__).parent / "figures"
    out.mkdir(exist_ok=True)
    path = out / "07_benchmark_complexity.pdf"
    fig.tight_layout()
    fig.savefig(path)
    fig.savefig(path.with_suffix(".png"), dpi=150)
    print(f"\nsaved: {path}")

    # --- seminar 行 100–103 の主張を数値的に示す ---
    print(f"\nn = 70 での n!: ≈ 10^{math.log10(math.factorial(70)):.0f}")


if __name__ == "__main__":
    main()
