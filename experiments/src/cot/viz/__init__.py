"""砂山 → 行き先 シナリオの可視化ユーティリティ.

`matplotlib` に依存する. `uv sync --extra viz` で導入される.
"""

from cot.viz.assignment_plot import (
    plot_assignment_2d,
    plot_cost_matrix,
    plot_enumeration_bar,
)
from cot.viz.config import use_japanese_font
from cot.viz.sandpile_plot import (
    plot_assignment_1d,
    plot_coupling_1d,
    plot_monge_map_1d,
    plot_sandpile_1d,
    plot_transport_plan_matrix,
)

__all__ = [
    "plot_assignment_1d",
    "plot_assignment_2d",
    "plot_cost_matrix",
    "plot_coupling_1d",
    "plot_enumeration_bar",
    "plot_monge_map_1d",
    "plot_sandpile_1d",
    "plot_transport_plan_matrix",
    "use_japanese_font",
]
