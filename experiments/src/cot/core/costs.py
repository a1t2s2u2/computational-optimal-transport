"""コスト行列の構築.

点集合 :math:`X = \\{x_i\\}_{i=1}^n \\subset \\mathbb{R}^d` と
:math:`Y = \\{y_j\\}_{j=1}^m \\subset \\mathbb{R}^d` に対して,
ground 距離 :math:`d(x_i, y_j)` の :math:`p` 乗をコストとする
:math:`C_{ij} = d(x_i, y_j)^p` を作る.
"""

from __future__ import annotations

import numpy as np

from cot.core.types import CostMatrix


def pairwise_distance_matrix(
    X: np.ndarray,
    Y: np.ndarray,
    p: float = 2.0,
) -> CostMatrix:
    """ペアワイズ距離の :math:`p` 乗からなるコスト行列を返す.

    Parameters
    ----------
    X : shape ``(n, d)``
        第一の点集合.
    Y : shape ``(m, d)``
        第二の点集合.
    p : float, default ``2.0``
        ground 距離のべき指数. ``p=2`` で平方ユークリッド距離, ``p=1`` でユークリッド距離.

    Returns
    -------
    C : shape ``(n, m)``
        :math:`C_{ij} = \\|x_i - y_j\\|_2^p`.
    """
    X = np.asarray(X, dtype=np.float64)
    Y = np.asarray(Y, dtype=np.float64)
    diff = X[:, None, :] - Y[None, :, :]
    dist = np.linalg.norm(diff, axis=-1)
    return dist**p
