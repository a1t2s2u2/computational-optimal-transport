"""全列挙による最適割当.

:math:`|\\mathrm{Perm}(n)| = n!` 通りの置換をすべて試し, 最小コストを与えるものを選ぶ.
教育目的 (``seminar §sem-assignment`` 行 24–126 の 3×3 例を再現) には十分だが,
:math:`n! \\geq 10^{100}\\ (n = 70)` から分かるように :math:`n \\geq 10` では実用不可.
"""

from __future__ import annotations

from collections.abc import Iterator
from itertools import permutations

import numpy as np

from cot.assignment.definitions import AssignmentProblem, AssignmentSolution


def solve_brute_force(problem: AssignmentProblem) -> AssignmentSolution:
    """:math:`n!` 通りの置換を全列挙し最適解を返す."""
    n = problem.n
    C = problem.C
    idx = np.arange(n)
    best_sigma: tuple[int, ...] | None = None
    best_raw = np.inf
    for perm in permutations(range(n)):
        raw = float(C[idx, perm].sum())
        if raw < best_raw:
            best_raw = raw
            best_sigma = perm
    assert best_sigma is not None
    return AssignmentSolution.from_sigma(np.array(best_sigma, dtype=np.int64), C)


def enumerate_all(problem: AssignmentProblem) -> Iterator[AssignmentSolution]:
    """全置換とそのコストを列挙 (seminar の表形式出力や棒グラフ用).

    Yields
    ------
    :class:`AssignmentSolution`
        各置換に対応する (最適とは限らない) 解オブジェクト.
    """
    n = problem.n
    C = problem.C
    for perm in permutations(range(n)):
        yield AssignmentSolution.from_sigma(np.array(perm, dtype=np.int64), C)
