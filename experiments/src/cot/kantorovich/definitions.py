"""離散 Kantorovich 問題の数学的対象を表す dataclass.

参照: `seminar/ch02_ot_foundations.tex` 行 444–563
------------------------------------------------------

離散カップリングの集合は

.. math::
   \\mathrm{CouplingsD}(\\mathbf{a}, \\mathbf{b}) \\defeq
   \\left\\{ \\mathbf{P} \\in \\mathbb{R}_+^{n \\times m} \\;\\middle|\\;
   \\mathbf{P} \\mathbf{1}_m = \\mathbf{a}, \\;
   \\mathbf{P}^\\top \\mathbf{1}_n = \\mathbf{b} \\right\\}

で定義される凸多面体. 目的関数は Frobenius 内積
:math:`\\langle \\mathbf{C}, \\mathbf{P} \\rangle = \\sum_{i,j} C_{ij} P_{ij}`.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from cot.core.scenario import SandpileScenario
from cot.core.types import CostMatrix, TransportPlan


@dataclass(frozen=True)
class KantorovichProblem:
    """離散 Kantorovich 問題.

    Parameters
    ----------
    a : shape ``(n,)``
        砂山の質量. :math:`\\sum_i a_i = 1`.
    b : shape ``(m,)``
        行き先の質量. :math:`\\sum_j b_j = 1`.
    C : shape ``(n, m)``
        コスト行列 :math:`C_{ij} = c(x_i, y_j)`.
    """

    a: np.ndarray
    b: np.ndarray
    C: CostMatrix

    def __post_init__(self) -> None:
        a = np.asarray(self.a, dtype=np.float64)
        b = np.asarray(self.b, dtype=np.float64)
        C = np.asarray(self.C, dtype=np.float64)
        if a.ndim != 1 or b.ndim != 1:
            raise ValueError("a, b は 1 次元配列でなければならない")
        if C.shape != (a.shape[0], b.shape[0]):
            raise ValueError(
                f"C must have shape (n={a.shape[0]}, m={b.shape[0]}), got {C.shape}"
            )
        if not np.isclose(a.sum(), b.sum()):
            raise ValueError(f"Σa = {a.sum()} must equal Σb = {b.sum()}")
        object.__setattr__(self, "a", a)
        object.__setattr__(self, "b", b)
        object.__setattr__(self, "C", C)

    @property
    def n(self) -> int:
        return int(self.a.shape[0])

    @property
    def m(self) -> int:
        return int(self.b.shape[0])

    @classmethod
    def from_scenario(
        cls, scenario: SandpileScenario, p: float = 1.0
    ) -> KantorovichProblem:
        """砂山シナリオからコスト行列を生成して問題を構築."""
        return cls(a=scenario.a, b=scenario.b, C=scenario.cost_matrix(p=p))


@dataclass(frozen=True)
class KantorovichSolution:
    """離散 Kantorovich 問題の解.

    Attributes
    ----------
    P : shape ``(n, m)``, dtype ``float64``
        最適な輸送計画 (カップリング行列). :math:`P_{ij}` は砂山 :math:`i` から
        行き先 :math:`j` へ送る質量.
    cost : float
        :math:`\\langle \\mathbf{C}, \\mathbf{P} \\rangle = \\sum_{ij} C_{ij} P_{ij}`.
    """

    P: TransportPlan
    cost: float

    @classmethod
    def from_plan(cls, P: np.ndarray, C: np.ndarray) -> KantorovichSolution:
        """輸送計画 ``P`` とコスト行列 ``C`` から解を構築."""
        P = np.asarray(P, dtype=np.float64)
        cost = float(np.sum(C * P))
        return cls(P=P, cost=cost)
