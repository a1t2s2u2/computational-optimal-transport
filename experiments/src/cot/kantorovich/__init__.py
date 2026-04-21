"""離散 Kantorovich 問題 (`seminar §sem-kantorovich`).

カップリング (結合測度) :math:`\\pi \\in \\Pi(\\alpha, \\beta)` のうち

.. math::
   \\int_{\\mathcal{X} \\times \\mathcal{Y}} c(x, y) \\, \\mathrm{d}\\pi(x, y)

を最小にするものを求める問題. 離散版は

.. math::
   \\min_{\\mathbf{P} \\in \\mathrm{CouplingsD}(\\mathbf{a}, \\mathbf{b})}
   \\langle \\mathbf{C}, \\mathbf{P} \\rangle

の有限次元線形計画になる (`ch02_ot_foundations.tex:543-563`).
"""

from cot.kantorovich.definitions import KantorovichProblem, KantorovichSolution
from cot.kantorovich.linprog import solve_linprog

__all__ = [
    "KantorovichProblem",
    "KantorovichSolution",
    "solve_linprog",
]
