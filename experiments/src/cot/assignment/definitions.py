"""最適割当問題の数学的対象を表す dataclass.

参照: `seminar/ch02_ot_foundations.tex` 行 15–22
------------------------------------------------

    定義 (最適割当問題).  コスト行列 :math:`C \\in \\mathbb{R}^{n \\times n}` に対し,

    .. math::
       \\min_{\\sigma \\in \\mathrm{Perm}(n)} \\frac{1}{n} \\sum_{i=1}^{n} C_{i,\\sigma(i)}

    を達成する置換 :math:`\\sigma` を求める.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from cot.core.types import CostMatrix, Permutation


@dataclass(frozen=True)
class AssignmentProblem:
    """最適割当問題.

    Parameters
    ----------
    C : shape ``(n, n)``
        コスト行列 :math:`C_{ij}` = 作業者 :math:`i` を仕事 :math:`j` に配属するコスト.
    """

    C: CostMatrix

    def __post_init__(self) -> None:
        C = np.asarray(self.C, dtype=np.float64)
        if C.ndim != 2 or C.shape[0] != C.shape[1]:
            raise ValueError(f"C must be a square matrix, got shape {C.shape}")
        object.__setattr__(self, "C", C)

    @property
    def n(self) -> int:
        return int(self.C.shape[0])


@dataclass(frozen=True)
class AssignmentSolution:
    """最適割当問題の解.

    Attributes
    ----------
    sigma : shape ``(n,)``, dtype ``int64``
        最適な置換 :math:`\\sigma`. **0-indexed**. すなわち ``sigma[i] = j`` は
        「作業者 :math:`i+1` を仕事 :math:`j+1` に割り当てる」を意味する.
    cost : float
        正規化済の最小コスト :math:`\\frac{1}{n} \\sum_i C_{i,\\sigma(i)}`.
    """

    sigma: Permutation
    cost: float

    @classmethod
    def from_sigma(cls, sigma: np.ndarray, C: np.ndarray) -> AssignmentSolution:
        """置換 ``sigma`` とコスト行列 ``C`` から解オブジェクトを構築."""
        sigma = np.asarray(sigma, dtype=np.int64)
        n = sigma.shape[0]
        cost = float(C[np.arange(n), sigma].sum()) / n
        return cls(sigma=sigma, cost=cost)

    def sigma_one_indexed(self) -> tuple[int, ...]:
        """seminar 原稿と同じ 1-indexed タプルで置換を返す (表示用)."""
        return tuple(int(j) + 1 for j in self.sigma)
