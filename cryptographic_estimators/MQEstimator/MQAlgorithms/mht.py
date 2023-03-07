from ...MQEstimator.mq_algorithm import MQAlgorithm
from ...MQEstimator.mq_problem import MQProblem
from ...helper import ComplexityType
from sage.all import Integer
from sage.arith.misc import is_power_of_two
from math import log2


class MHT(MQAlgorithm):
    r"""
    Construct an instance of MHT estimator

    The MHT is an algorithm to solve the MQ problem when  $m  (m + 3) / 2 \leq n$ [MHT13]_.

    INPUT:

    - ``problem`` -- MQProblem object including all necessary parameters
    - ``w`` -- linear algebra constant (2 <= w <= 3) (default: 2)
    - ``memory_access`` -- specifies the memory access cost model (default: 0, choices: 0 - constant, 1 - logarithmic, 2 - square-root, 3 - cube-root or deploy custom function which takes as input the logarithm of the total memory usage)
    - ``complexity_type`` -- complexity type to consider (0: estimate, 1: tilde O comp

    EXAMPLES::

        sage: from cryptographic_estimators.MQEstimator.MQAlgorithms.mht import MHT
        sage: from cryptographic_estimators.MQEstimator.mq_problem import MQProblem
        sage: E = MHT(MQProblem(n=183, m=12, q=4), w=2.8)
        sage: E
        MHT estimator for the MQ problem with 183 variables and 12 polynomials

    TESTS::

        sage: E.problem.nvariables() == E.nvariables_reduced()
        True
    """
    def __init__(self, problem: MQProblem, **kwargs):
        n, m, q = problem.get_problem_parameters()
        if not isinstance(q, (int, Integer)):
            raise TypeError("q must be an integer")

        if m * (m + 3) / 2 > n:
            raise ValueError(f'The parameter n should be grater than or equal to m * (m + 3) / 2')

        super().__init__(problem, **kwargs)
        self._name = "MHT"
        self._n_reduced = n
        self._m_reduced = m

    def time_complexity(self):
        """
        Return the time complexity of mht algorithm

        EXAMPLES::

            sage: from cryptographic_estimators.MQEstimator.MQAlgorithms.mht import MHT
            sage: from cryptographic_estimators.MQEstimator.mq_problem import MQProblem
            sage: E = MHT(MQProblem(n=183, m=12, q=4), w=2.8)
            sage: E.time_complexity()
            24.628922047916475
        """
        n, m, _ = self.problem.get_problem_parameters()
        w = self.linear_algebra_constant()
        if is_power_of_two(self.problem.order_of_the_field()):
            time = 0
        else:
            time = m
        if self.complexity_type == ComplexityType.ESTIMATE.value:
            time += log2(m * n ** w)
        else:
            time += 0
        return time

    def memory_complexity(self):
        """
        Return the memory complexity of MHT algorithm

        EXAMPLES::

            sage: from cryptographic_estimators.MQEstimator.MQAlgorithms.mht import MHT
            sage: from cryptographic_estimators.MQEstimator.mq_problem import MQProblem
            sage: E = MHT(MQProblem(n=183, m=12, q=4), w=2.8)
            sage: E.memory_complexity()
            18.61636217728924
        """
        n, m, q = self.problem.get_problem_parameters()
        if self.complexity_type == ComplexityType.ESTIMATE.value:
            memory = log2(m * n ** 2)
        else:
            memory = 0
        return memory

