"""全写像列挙による離散 Monge 問題の解法.

:math:`m^n` 通りの写像 :math:`T \\colon \\{x_1, \\ldots, x_n\\} \\to \\{y_1, \\ldots, y_m\\}`
を列挙し, 押し出し条件

.. math::
   \\forall j\\colon\\quad \\sum_{i\\,:\\,T(x_i) = y_j} a_i = b_j

(命題 sem-dirac-pushforward) を満たすもののうち最小コストを返す.

特に :math:`n = m`, :math:`a = b = (1/n)\\mathbf{1}` の場合, 押し出し条件を通る
写像は全単射 (置換) に限られ, 最適割当問題に帰着する
(`ch02_ot_foundations.tex:201-213`).
"""

from __future__ import annotations

from collections.abc import Iterator
from itertools import product

import numpy as np

from cot.monge.definitions import MongeProblem, MongeSolution


def _is_feasible(T_idx: np.ndarray, a: np.ndarray, b: np.ndarray) -> bool:
    """押し出し条件 :math:`T\\pushforward \\alpha = \\beta` (離散版) を検査."""
    m = b.shape[0]
    pushed = np.zeros(m, dtype=np.float64)
    for i, j in enumerate(T_idx):
        pushed[int(j)] += a[i]
    return bool(np.allclose(pushed, b))


def enumerate_feasible(problem: MongeProblem) -> Iterator[MongeSolution]:
    """押し出し条件を満たす全写像とそのコストを列挙する (教育・可視化用).

    Yields
    ------
    :class:`MongeSolution`
        実行可能な写像に対応する解オブジェクト (最適とは限らない).
    """
    n, m = problem.n, problem.m
    a, b = problem.scenario.a, problem.scenario.b
    C = problem.C
    for T_tuple in product(range(m), repeat=n):
        T_idx = np.array(T_tuple, dtype=np.int64)
        if _is_feasible(T_idx, a, b):
            yield MongeSolution.from_map(T_idx, a, C)


def solve_brute_force(problem: MongeProblem) -> MongeSolution:
    """全 :math:`m^n` 写像を列挙し, 押出可能な最小コストを達成する解を返す.

    Raises
    ------
    ValueError
        押し出し条件を満たす写像が一つも存在しない場合
        (`ch02_ot_foundations.tex:371-417`: Monge 写像の非存在).
    """
    best: MongeSolution | None = None
    for sol in enumerate_feasible(problem):
        if best is None or sol.cost < best.cost:
            best = sol
    if best is None:
        raise ValueError(
            "押し出し条件 T#α = β を満たす写像 T が存在しない. "
            "Kantorovich 緩和を用いること (§sem-kantorovich)."
        )
    return best
