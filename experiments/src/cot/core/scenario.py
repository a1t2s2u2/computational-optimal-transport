"""砂山 → 行き先 の離散輸送シナリオ.

seminar `ch02_ot_foundations.tex` 全章で用いる共通の題材をひとまとめにする.

    砂山 :math:`\\alpha = \\sum_{i=1}^n a_i \\delta_{x_i}` が位置 :math:`x_i` にあり,
    行き先 :math:`\\beta = \\sum_{j=1}^m b_j \\delta_{y_j}` が位置 :math:`y_j` にある.
    :math:`c(x, y) = \\|x - y\\|_2^p` をコストとして, 総輸送コストを最小化する
    `割当 / Monge / Kantorovich` の 3 問題はすべてこのシナリオから構築される.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from cot.core.costs import pairwise_distance_matrix
from cot.core.types import CostMatrix


@dataclass(frozen=True)
class SandpileScenario:
    """砂山 → 行き先 の離散シナリオ.

    Attributes
    ----------
    x : shape ``(n,)`` または ``(n, d)``
        砂山の位置. 1 次元の場合は shape ``(n,)`` を許容する.
    y : shape ``(m,)`` または ``(m, d)``
        行き先の位置.
    a : shape ``(n,)``
        砂山の質量 :math:`(a_1, \\ldots, a_n)`. 確率測度なので
        :math:`\\sum_i a_i = 1`.
    b : shape ``(m,)``
        行き先の質量 :math:`(b_1, \\ldots, b_m)`. :math:`\\sum_j b_j = 1`.
    """

    x: np.ndarray
    y: np.ndarray
    a: np.ndarray
    b: np.ndarray

    def __post_init__(self) -> None:
        x = np.asarray(self.x, dtype=np.float64)
        y = np.asarray(self.y, dtype=np.float64)
        a = np.asarray(self.a, dtype=np.float64)
        b = np.asarray(self.b, dtype=np.float64)

        if x.ndim not in (1, 2):
            raise ValueError(f"x must be 1D or 2D, got shape {x.shape}")
        if y.ndim not in (1, 2):
            raise ValueError(f"y must be 1D or 2D, got shape {y.shape}")
        if a.ndim != 1 or a.shape[0] != x.shape[0]:
            raise ValueError(f"a must be 1D of length n={x.shape[0]}, got shape {a.shape}")
        if b.ndim != 1 or b.shape[0] != y.shape[0]:
            raise ValueError(f"b must be 1D of length m={y.shape[0]}, got shape {b.shape}")
        if np.any(a < 0) or np.any(b < 0):
            raise ValueError("masses a, b must be non-negative")
        if not np.isclose(a.sum(), 1.0):
            raise ValueError(f"a must sum to 1, got {a.sum()}")
        if not np.isclose(b.sum(), 1.0):
            raise ValueError(f"b must sum to 1, got {b.sum()}")

        object.__setattr__(self, "x", x)
        object.__setattr__(self, "y", y)
        object.__setattr__(self, "a", a)
        object.__setattr__(self, "b", b)

    @property
    def n(self) -> int:
        """砂山の数."""
        return int(self.x.shape[0])

    @property
    def m(self) -> int:
        """行き先の数."""
        return int(self.y.shape[0])

    def cost_matrix(self, p: float = 1.0) -> CostMatrix:
        """コスト行列 :math:`C_{ij} = \\|x_i - y_j\\|_2^p` を返す.

        seminar §sem-assignment 例は 1 次元かつ :math:`p=1`
        (絶対値 :math:`|x_i - y_j|`) を採用する.
        """
        x = self.x if self.x.ndim == 2 else self.x.reshape(-1, 1)
        y = self.y if self.y.ndim == 2 else self.y.reshape(-1, 1)
        return pairwise_distance_matrix(x, y, p=p)

    @property
    def is_balanced_uniform(self) -> bool:
        """:math:`n = m` かつ :math:`a = b = (1/n)\\mathbf{1}` か."""
        if self.n != self.m:
            return False
        return bool(
            np.allclose(self.a, 1.0 / self.n) and np.allclose(self.b, 1.0 / self.n)
        )


def seminar_n2_scenario() -> SandpileScenario:
    """seminar §sem-assignment 例 (ch02_ot_foundations.tex 行 27–98) の n=2 シナリオ.

    1 次元の直線上に 2 つの砂山と 2 つの行き先を配置:

    ==========  =============  =============
    名称        位置            質量
    ==========  =============  =============
    砂山 x_1    :math:`0`       :math:`1/2`
    砂山 x_2    :math:`3`       :math:`1/2`
    行き先 y_1  :math:`1`       :math:`1/2`
    行き先 y_2  :math:`4`       :math:`1/2`
    ==========  =============  =============

    :math:`p = 1` のコストは :math:`C = \\begin{pmatrix}1 & 4 \\\\ 2 & 1\\end{pmatrix}` で,
    最適割当は :math:`\\sigma^\\star = (1, 2)` (交差しない対応), コスト :math:`1`.
    """
    return SandpileScenario(
        x=np.array([0.0, 3.0]),
        y=np.array([1.0, 4.0]),
        a=np.array([0.5, 0.5]),
        b=np.array([0.5, 0.5]),
    )
