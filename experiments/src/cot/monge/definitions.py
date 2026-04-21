"""離散 Monge 問題の数学的対象を表す dataclass.

参照: `seminar/ch02_ot_foundations.tex` 行 169–199
------------------------------------------------------

    離散 Monge 問題.  確率測度
    :math:`\\alpha = \\sum_i a_i \\delta_{x_i}`,
    :math:`\\beta = \\sum_j b_j \\delta_{y_j}` に対し,

    .. math::
       \\min_{T} \\left\\{
       \\sum_{i=1}^{n} a_i \\, c(x_i, T(x_i))
       \\;\\middle|\\;
       T\\pushforward \\alpha = \\beta
       \\right\\}

    を達成する写像 :math:`T` を求める.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

from cot.core.scenario import SandpileScenario
from cot.core.types import CostMatrix, MongeMap


@dataclass(frozen=True)
class MongeProblem:
    """離散 Monge 問題.

    Parameters
    ----------
    scenario : SandpileScenario
        砂山 :math:`(x_i, a_i)` と行き先 :math:`(y_j, b_j)`.
    C : shape ``(n, m)``, optional
        コスト行列. 省略時は ``scenario.cost_matrix(p)`` から生成.
    p : float, default ``1.0``
        ``C`` 省略時の ground 距離の指数 :math:`C_{ij} = \\|x_i - y_j\\|_2^p`.
    """

    scenario: SandpileScenario
    C: CostMatrix = field(default=None)  # type: ignore[assignment]
    p: float = 1.0

    def __post_init__(self) -> None:
        if self.C is None:
            object.__setattr__(self, "C", self.scenario.cost_matrix(p=self.p))
        else:
            C = np.asarray(self.C, dtype=np.float64)
            n, m = self.scenario.n, self.scenario.m
            if C.shape != (n, m):
                raise ValueError(f"C must have shape ({n}, {m}), got {C.shape}")
            object.__setattr__(self, "C", C)

    @property
    def n(self) -> int:
        return self.scenario.n

    @property
    def m(self) -> int:
        return self.scenario.m


@dataclass(frozen=True)
class MongeSolution:
    """離散 Monge 問題の解.

    Attributes
    ----------
    T_idx : shape ``(n,)``, dtype ``int64``
        写像 :math:`T` の添字表現. ``T_idx[i] = j`` は :math:`T(x_i) = y_j` を意味する
        (**0-indexed**).
    cost : float
        :math:`\\sum_i a_i \\, C_{i, T(i)}`.
    """

    T_idx: MongeMap
    cost: float

    @classmethod
    def from_map(cls, T_idx: np.ndarray, a: np.ndarray, C: np.ndarray) -> MongeSolution:
        """写像 ``T_idx``, 質量 ``a``, コスト ``C`` から解を構築."""
        T_idx = np.asarray(T_idx, dtype=np.int64)
        n = T_idx.shape[0]
        cost = float(np.sum(a * C[np.arange(n), T_idx]))
        return cls(T_idx=T_idx, cost=cost)

    def t_one_indexed(self) -> tuple[int, ...]:
        """seminar 原稿と同じ 1-indexed タプルで写像 :math:`T` を返す (表示用).

        例: ``T_idx = (0, 1)`` → ``(1, 2)`` (= "x_1 → y_1, x_2 → y_2").
        """
        return tuple(int(j) + 1 for j in self.T_idx)
