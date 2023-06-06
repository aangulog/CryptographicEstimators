

from ...MQEstimator.mq_algorithm import MQAlgorithm
from ...MQEstimator.mq_problem import MQProblem
from ...helper import ComplexityType
from math import log2
from sage.all import Integer
from sage.arith.misc import is_power_of_two


class KPG(MQAlgorithm):
    r"""
    Construct an instance of KPG estimator

    The KPG is an algorithm to solve a quadratic systems of equations over fields of even characteristic [KPG99]_.

    INPUT:

    - ``problem`` -- MQProblem object including all necessary parameters
    - ``w`` -- linear algebra constant (2 <= w <= 3) (default: 2)
    - ``memory_access`` -- specifies the memory access cost model (default: 0, choices: 0 - constant, 1 - logarithmic, 2 - square-root, 3 - cube-root or deploy custom function which takes as input the logarithm of the total memory usage)
    - ``complexity_type`` -- complexity type to consider (0: estimate, 1: tilde O comp

    EXAMPLES::

        sage: from cryptographic_estimators.MQEstimator.MQAlgorithms.kpg import KPG
        sage: from cryptographic_estimators.MQEstimator.mq_problem import MQProblem
        sage: E = KPG(MQProblem(n=183, m=12, q=4), w=2.8)
        sage: E
        KPG estimator for the MQ problem with 183 variables and 12 polynomials

    TESTS::

        sage: E.problem.nvariables() == E.nvariables_reduced()
        True
    """

    def __init__(self, problem: MQProblem, **kwargs):
        n, m, q = problem.get_problem_parameters()
        if not isinstance(q, (int, Integer)):
            raise TypeError("q must be an integer")

        if not is_power_of_two(q):
            raise ValueError(
                "the order of finite field q must be a power of 2")

        if m * (m + 1) >= n:
            raise ValueError(f'The condition m(m + 1) < n must be satisfied')

        super().__init__(problem, **kwargs)
        self._name = "KPG"
        self._n_reduced = n
        self._m_reduced = m

    def _compute_time_complexity(self, parameters: dict):
        """
        Return the time complexity of the algorithm for a given set of parameters

        TESTS::

            sage: from cryptographic_estimators.MQEstimator.MQAlgorithms.kpg import KPG
            sage: from cryptographic_estimators.MQEstimator.mq_problem import MQProblem
            sage: E = KPG(MQProblem(n=183, m=12, q=4), w=2.8)
            sage: E.time_complexity()
            26.628922047916475
        """
        n, m, _ = self.problem.get_problem_parameters()
        w = self.linear_algebra_constant()
        return log2(m * n ** w)

    def _compute_memory_complexity(self, parameters: dict):
        """
        Return the memory complexity of the algorithm for a given set of parameters

        TESTS::

            sage: from cryptographic_estimators.MQEstimator.MQAlgorithms.kpg import KPG
            sage: from cryptographic_estimators.MQEstimator.mq_problem import MQProblem
            sage: E = KPG(MQProblem(n=183, m=12, q=4), w=2.8)
            sage: E.memory_complexity()
            19.61636217728924
        """
        n, m, _ = self.problem.get_problem_parameters()
        return log2(m * n ** 2)

    def _compute_tilde_o_time_complexity(self, parameters: dict):
        """
        Return the Ō time complexity of the algorithm for a given set of parameters

        """
        return 0

    def _compute_tilde_o_memory_complexity(self, parameters: dict):
        """
        Return the Ō memory complexity of the algorithm for a given set of parameters

        INPUT:

        - ``parameters`` -- dictionary including the parameters

        """
        return 0
