"""型エイリアス.

seminar の記法 (`preamble.tex`) に対応:
- :math:`C \\in \\mathbb{R}^{n \\times m}` → :data:`CostMatrix`
- :math:`\\sigma \\in \\mathrm{Perm}(n)` → :data:`Permutation` (0-indexed)
"""

from __future__ import annotations

import numpy as np
import numpy.typing as npt

CostMatrix = npt.NDArray[np.float64]
Permutation = npt.NDArray[np.int64]
