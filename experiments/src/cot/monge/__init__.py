"""離散 Monge 問題 (`seminar §sem-monge`).

砂山の分布 :math:`\\alpha = \\sum_i a_i \\delta_{x_i}` を
行き先の分布 :math:`\\beta = \\sum_j b_j \\delta_{y_j}` に押し出す
可測写像 :math:`T` のうち, 総輸送コスト

.. math::
   \\sum_{i=1}^{n} a_i \\, c(x_i, T(x_i))

を最小にするものを求める問題 (`ch02_ot_foundations.tex:190-199`).
"""

from cot.monge.brute_force import enumerate_feasible, solve_brute_force
from cot.monge.definitions import MongeProblem, MongeSolution

__all__ = [
    "MongeProblem",
    "MongeSolution",
    "enumerate_feasible",
    "solve_brute_force",
]
