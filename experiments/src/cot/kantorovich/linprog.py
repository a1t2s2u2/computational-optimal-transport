"""``scipy.optimize.linprog`` による離散 Kantorovich 問題の解法.

行列変数 :math:`\\mathbf{P} \\in \\mathbb{R}_+^{n \\times m}` をベクトル化
:math:`\\mathrm{vec}(\\mathbf{P}) \\in \\mathbb{R}^{nm}` して LP に書き下す:

.. math::
   \\min_{p \\geq 0} \\; c^\\top p
   \\quad \\text{s.t.} \\quad A_{\\mathrm{eq}}\\, p = d

ここで

* :math:`c = \\mathrm{vec}(\\mathbf{C})` — 目的係数.
* 行和制約 :math:`\\mathbf{P} \\mathbf{1}_m = \\mathbf{a}` は
  :math:`A_r = I_n \\otimes \\mathbf{1}_m^\\top \\in \\mathbb{R}^{n \\times nm}`.
* 列和制約 :math:`\\mathbf{P}^\\top \\mathbf{1}_n = \\mathbf{b}` は
  :math:`A_c = \\mathbf{1}_n^\\top \\otimes I_m \\in \\mathbb{R}^{m \\times nm}`.

:math:`\\sum_i a_i = \\sum_j b_j = 1` より上記 :math:`n + m` 本の等式のうち 1 本は
冗長になるため, 最後の列和制約を落として
:math:`A_{\\mathrm{eq}} \\in \\mathbb{R}^{(n + m - 1) \\times nm}` を作る
(scipy の HiGHS は冗長制約をそのまま与えても動くが, 念のため縮退回避).
"""

from __future__ import annotations

import numpy as np
from scipy.optimize import linprog

from cot.kantorovich.definitions import KantorovichProblem, KantorovichSolution


def _build_equality_constraints(
    n: int, m: int, a: np.ndarray, b: np.ndarray
) -> tuple[np.ndarray, np.ndarray]:
    """等式制約 :math:`A_{\\mathrm{eq}} p = d` を組む.

    Returns
    -------
    A_eq : shape ``(n + m - 1, n * m)``
    d    : shape ``(n + m - 1,)``
    """
    A_r = np.kron(np.eye(n), np.ones((1, m)))
    A_c = np.kron(np.ones((1, n)), np.eye(m))
    # 列和制約は m 本のうち最後の 1 本を落として冗長性を除く.
    A_eq = np.vstack([A_r, A_c[:-1, :]])
    d = np.concatenate([a, b[:-1]])
    return A_eq, d


def solve_linprog(problem: KantorovichProblem) -> KantorovichSolution:
    """``scipy.optimize.linprog`` (HiGHS) で LP を解き, 輸送計画 :math:`\\mathbf{P}` を返す."""
    n, m = problem.n, problem.m
    c = problem.C.ravel()
    A_eq, d = _build_equality_constraints(n, m, problem.a, problem.b)
    result = linprog(
        c=c,
        A_eq=A_eq,
        b_eq=d,
        bounds=(0.0, None),
        method="highs",
    )
    if not result.success:
        raise RuntimeError(f"linprog failed: {result.message}")
    P = result.x.reshape(n, m)
    # HiGHS は微小な負値 (-1e-16 など) を返すことがあるため非負にクリップ.
    P = np.where(np.abs(P) < 1e-12, 0.0, P)
    return KantorovichSolution.from_plan(P, problem.C)
