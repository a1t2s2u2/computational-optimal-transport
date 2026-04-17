"""最適割当の可視化ユーティリティ.

`matplotlib` に依存する. `uv sync --extra viz` で導入される.
"""

from cot.viz.assignment_plot import (
    plot_assignment_2d,
    plot_cost_matrix,
    plot_enumeration_bar,
)
from cot.viz.config import use_japanese_font

__all__ = [
    "plot_assignment_2d",
    "plot_cost_matrix",
    "plot_enumeration_bar",
    "use_japanese_font",
]
