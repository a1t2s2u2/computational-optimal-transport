"""ハンガリアン法による最適割当.

``scipy.optimize.linear_sum_assignment`` (Jonker–Volgenant アルゴリズム) を薄くラップする.
計算量は :math:`O(n^3)` で, :math:`n!` 爆発する全列挙に対し実用的な解法
(``seminar §sem-assignment`` 行 128–132 で言及).

seminar の正規化コスト :math:`\\frac{1}{n}\\sum_i C_{i,\\sigma(i)}` と scipy が返す
生の和 :math:`\\sum_i C_{i,\\sigma(i)}` は **係数 ``1/n`` の違い** があることに注意.
本ラッパは正規化コストを返す.
"""

from __future__ import annotations

import numpy as np
from scipy.optimize import linear_sum_assignment

from cot.assignment.definitions import AssignmentProblem, AssignmentSolution


def solve_hungarian(problem: AssignmentProblem) -> AssignmentSolution:
    """ハンガリアン法で最適割当 :math:`\\sigma` を求める."""
    row_ind, col_ind = linear_sum_assignment(problem.C)
    assert np.array_equal(row_ind, np.arange(problem.n))
    sigma = np.asarray(col_ind, dtype=np.int64)
    return AssignmentSolution.from_sigma(sigma, problem.C)
