"""型エイリアス.

seminar の記法 (`preamble.tex`) に対応:
- :math:`C \\in \\mathbb{R}^{n \\times m}` → :data:`CostMatrix`
- :math:`\\sigma \\in \\mathrm{Perm}(n)` → :data:`Permutation` (0-indexed)
- :math:`P \\in \\mathbb{R}_+^{n \\times m}` (離散カップリング) → :data:`TransportPlan`
- 離散 Monge 写像 :math:`T` を添字配列で表す → :data:`MongeMap`
"""

from __future__ import annotations

import numpy as np
import numpy.typing as npt

CostMatrix = npt.NDArray[np.float64]
Permutation = npt.NDArray[np.int64]
TransportPlan = npt.NDArray[np.float64]
MongeMap = npt.NDArray[np.int64]
