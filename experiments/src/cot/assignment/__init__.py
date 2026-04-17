"""最適割当問題 (`seminar §sem-assignment`).

コスト行列 :math:`C \\in \\mathbb{R}^{n \\times n}` に対し

.. math::
   \\min_{\\sigma \\in \\mathrm{Perm}(n)} \\frac{1}{n} \\sum_{i=1}^{n} C_{i,\\sigma(i)}

を解く置換 :math:`\\sigma` を求める問題.
"""

from cot.assignment.brute_force import solve_brute_force
from cot.assignment.definitions import AssignmentProblem, AssignmentSolution
from cot.assignment.hungarian import solve_hungarian

__all__ = [
    "AssignmentProblem",
    "AssignmentSolution",
    "solve_brute_force",
    "solve_hungarian",
]
