"""離散測度 (ヒストグラム) の生成.

seminar では確率単体 :math:`\\Sigma_n = \\{a \\in \\mathbb{R}^n_+ \\mid \\sum_i a_i = 1\\}`
(`preamble.tex` の ``\\simplex``) を扱う. 最適割当問題では :math:`a = b = \\mathbf{1}_n / n`
のみが必要となる.
"""

from __future__ import annotations

import numpy as np

from cot.core.types import Histogram


def uniform(n: int) -> Histogram:
    """一様ヒストグラム :math:`\\mathbf{1}_n / n \\in \\Sigma_n` を返す."""
    if n <= 0:
        raise ValueError(f"n must be positive, got {n}")
    return np.full(n, 1.0 / n, dtype=np.float64)
