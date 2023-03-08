from ...MQEstimator.mq_algorithm import MQAlgorithm
from ...MQEstimator.mq_problem import MQProblem
from ...MQEstimator.series.hilbert import HilbertSeries
from ...MQEstimator.series.nmonomial import NMonomialSeries
from ...MQEstimator.mq_helper import nmonomials_up_to_degree
from ...base_algorithm import optimal_parameter
from math import log2
from sage.all import Integer
from sage.rings.all import QQ
from sage.rings.infinity import Infinity
from sage.rings.power_series_ring import PowerSeriesRing
from sage.functions.other import binomial


class Crossbred(MQAlgorithm):
    r"""
    Construct an instance of crossbred estimator

    The Crossbred is an algorithm to solve the MQ problem [JV18]_. This algorithm consists of two steps, named the
    preprocessing step and the linearization step. In the preprocessing step, we find a set $S$ of degree-$D$
    polynomials in the ideal generated by the initial set of polynomials. Every specialization  of the first $n-k$
    variables of the polynomials in $S$ results in a set $S'$ of degree-$d$ polynomials in $k$ variables. Finally, in
    the linearization step, a solution to $S'$ is found by direct linearization.

    .. NOTE::

        Our complexity estimates are a generalization over any field of size `q` of the complexity formulas given in
        [Dua20]_, which are given either for `q=2` or generic fields.

    INPUT:

    - ``problem`` -- MQProblem object including all necessary parameters
    - ``h`` -- external hybridization parameter (default: 0)
    - ``w`` -- linear algebra constant (2 <= w <= 3) (default: 2)
    - ``max_D`` -- upper bound to the parameter D (default: 20)
    - ``memory_access`` -- specifies the memory access cost model (default: 0, choices: 0 - constant, 1 - logarithmic, 2 - square-root, 3 - cube-root or deploy custom function which takes as input the logarithm of the total memory usage)
    - ``complexity_type`` -- complexity type to consider (0: estimate, 1: tilde O complexity, default: 0)

    EXAMPLES::

        sage: from cryptographic_estimators.MQEstimator.MQAlgorithms.crossbred import Crossbred
        sage: from cryptographic_estimators.MQEstimator.mq_problem import MQProblem
        sage: E = Crossbred(MQProblem(n=10, m=12, q=5))
        sage: E
        Crossbred estimator for the MQ problem with 10 variables and 12 polynomials
    """

    def __init__(self, problem: MQProblem, **kwargs):
        q = problem.order_of_the_field()
        if not isinstance(q, (int, Integer)):
            raise TypeError("q must be an integer")

        super(Crossbred, self).__init__(problem, **kwargs)
        self._name = "Crossbred"
        self._max_D = kwargs.get('max_D', min(30, min(problem.nvariables(), problem.npolynomials())))
        if not isinstance(self._max_D, (int, Integer)):
            raise TypeError("max_D must be an integer")

        n = self.nvariables_reduced()
        self.set_parameter_ranges('k', 1, n)
        self.set_parameter_ranges('D', 2, self._max_D)
        self.set_parameter_ranges('d', 1, n)



    @optimal_parameter
    def k(self):
        """
        Return the optimal `k`, i.e. no. of variables in the resulting system

        EXAMPLES::

            sage: from cryptographic_estimators.MQEstimator.MQAlgorithms.crossbred import Crossbred
            sage: from cryptographic_estimators.MQEstimator.mq_problem import MQProblem
            sage: E = Crossbred(MQProblem(n=10, m=12, q=5))
            sage: E.k()
            7
        """
        return self._get_optimal_parameter('k')

    @optimal_parameter
    def D(self):
        """
        Return the optimal `D`, i.e. degree of the initial Macaulay matrix

        EXAMPLES::

            sage: from cryptographic_estimators.MQEstimator.MQAlgorithms.crossbred import Crossbred
            sage: from cryptographic_estimators.MQEstimator.mq_problem import MQProblem
            sage: E = Crossbred(MQProblem(n=10, m=12, q=5), max_D = 10)
            sage: E.D()
            5
        """
        return self._get_optimal_parameter('D')

    @optimal_parameter
    def d(self):
        """
        Return the optimal `d`, i.e. degree resulting Macaulay matrix

        EXAMPLES::

            sage: from cryptographic_estimators.MQEstimator.MQAlgorithms.crossbred import Crossbred
            sage: from cryptographic_estimators.MQEstimator.mq_problem import MQProblem
            sage: E = Crossbred(MQProblem(n=10, m=12, q=5), max_D = 10)
            sage: E.d()
            1
        """
        return self._get_optimal_parameter('d')

    @property
    def max_D(self):
        """
        Return the upper bound of the degree of the initial Macaulay matrix

        EXAMPLES::

            sage: from cryptographic_estimators.MQEstimator.MQAlgorithms.crossbred import Crossbred
            sage: from cryptographic_estimators.MQEstimator.mq_problem import MQProblem
            sage: E = Crossbred(MQProblem(n=10, m=12, q=5))
            sage: E.max_D
            10
        """
        return self._max_D

    @max_D.setter
    def max_D(self, value):
        """
        Set new upper bound of the degree of the initial Macaulay matrix

        INPUT:

        - ``value`` -- integer to be set as the upper bound of the parameter `D`
        """
        self.reset()
        min_D = self._parameter_ranges['D']['min']
        self._max_D = value
        self.set_parameter_ranges('D', min_D, value)

    def _ncols_in_preprocessing_step(self, k, D, d):
        """
        Return the number of columns involve in the preprocessing step

        INPUT:

        - ``k`` -- no. variables in the resulting system
        - ``D`` -- degree of the initial Macaulay matrix
        - ``d`` -- degree resulting Macaulay matrix

        EXAMPLES::

            sage: from cryptographic_estimators.MQEstimator.MQAlgorithms.crossbred import Crossbred
            sage: from cryptographic_estimators.MQEstimator.mq_problem import MQProblem
            sage: E = Crossbred(MQProblem(n=10, m=12, q=5))
            sage: E._ncols_in_preprocessing_step(4, 6, 3)
            297
        """
        if d >= D:
            raise ValueError("d must be smaller than D")

        n, _, q = self.get_reduced_parameters()
        nms0 = NMonomialSeries(n=k, q=q, max_prec=D + 1)
        nms1 = NMonomialSeries(n=n - k, q=q, max_prec=D + 1)

        ncols = 0
        for dk in range(d + 1, D):
            ncols += sum([nms0.nmonomials_of_degree(dk) * nms1.nmonomials_of_degree(dp) for dp in range(D - dk)])

        return ncols

    def _ncols_in_linearization_step(self, k, d):
        """
        Return the number of columns involve in the linearization step

        INPUT:

        - ``k`` -- no. variables in the resulting system
        - ``d`` -- degree resulting Macaulay matrix

        EXAMPLES::

            sage: from cryptographic_estimators.MQEstimator.MQAlgorithms.crossbred import Crossbred
            sage: from cryptographic_estimators.MQEstimator.mq_problem import MQProblem
            sage: E = Crossbred(MQProblem(n=10, m=12, q=5))
            sage: E._ncols_in_linearization_step(4, 3)
            35
        """
        return nmonomials_up_to_degree(d, k, q=self.problem.order_of_the_field())

    def _admissible_parameter_series(self, k):
        """
        Return a the series $S_k$ of admissible parameters

        INPUT:

        - ``k`` -- no. variables in the resulting system

        EXAMPLES::

            sage: from cryptographic_estimators.MQEstimator.MQAlgorithms.crossbred import Crossbred
            sage: from cryptographic_estimators.MQEstimator.mq_problem import MQProblem
            sage: E = Crossbred(MQProblem(n=10, m=12, q=5), max_D = 2)
            sage: E._admissible_parameter_series(2)
            -1 - 3*x - 3*y - 10*x^2 - 3*x*y + 6*y^2 + O(x, y)^3
        """
        n, m, q = self.get_reduced_parameters()
        max_D = self.max_D

        R = PowerSeriesRing(QQ, names=['x', 'y'], default_prec=max_D + 1)
        x, y = R.gens()

        Hk = HilbertSeries(n=k, degrees=[2] * m, q=q)
        k_y, k_xy = Hk.series(y), Hk.series(x * y)

        Hn = HilbertSeries(n=n, degrees=[2] * m, q=q)
        n_x = Hn.series(x)

        N = NMonomialSeries(n=n - k, q=q, max_prec=max_D + 1)
        nk_x = N.series_monomials_of_degree()(x)

        return (k_xy * nk_x - n_x - k_y) / ((1 - x) * (1 - y))

    def _valid_choices(self):
        """
        Return a list of admissible parameters `(k, D, d)`

        EXAMPLES::

            sage: from cryptographic_estimators.MQEstimator.MQAlgorithms.crossbred import Crossbred
            sage: from cryptographic_estimators.MQEstimator.mq_problem import MQProblem
            sage: E = Crossbred(MQProblem(n=10, m=12, q=5))
            sage: [list(x.values()) for x in E._valid_choices()][:5] == [[2, 1, 1], [3, 1, 1], [4, 1, 1], [3, 2, 1], [5, 1, 1]]
            True
        """
        parameters = self._optimal_parameters
        ranges = self._parameter_ranges
        new_ranges = {i: ranges[i].copy() if i not in parameters else {"min": parameters[i], "max": parameters[i]}
                      for i in ranges}

        k = 1
        stop = False
        while not stop:
            Sk = self._admissible_parameter_series(k)
            for (monomial, coefficient) in Sk.coefficients().items():
                D, d = monomial.exponents()[0]
                if 0 <= coefficient and d < D and new_ranges['D']["min"] <= D <= new_ranges['D']["max"] and new_ranges['d']["min"] <= d <= new_ranges['d']["max"]:
                    yield {'D': D, 'd': d, 'k': k}

            k += 1
            if k > new_ranges['k']["max"]:
                stop = True

    def _compute_time_complexity(self, parameters):
        """
        Return the time complexity of the algorithm for a given set of parameters

        INPUT:

        - ``parameters`` -- dictionary including the parameters

        TESTS::

            sage: from cryptographic_estimators.MQEstimator.MQAlgorithms.crossbred import Crossbred
            sage: from cryptographic_estimators.MQEstimator.mq_problem import MQProblem
            sage: E = Crossbred(MQProblem(n=10, m=12, q=5))
            sage: E._compute_time_complexity({'k': 4, 'D': 6, 'd':4})
            29.77510134996699

            sage: E = Crossbred(MQProblem(n=10, m=12, q=5), bit_complexities=False)
            sage: E.time_complexity()
            19.56992234329735
        """
        k = parameters['k']
        D = parameters['D']
        d = parameters['d']
        n, m, q = self.get_reduced_parameters()
        w = self.linear_algebra_constant()
        np = self._ncols_in_preprocessing_step(k=k, D=D, d=d)
        nl = self._ncols_in_linearization_step(k=k, d=d)
        complexity_wiedemann = 3 * binomial(k + d, d) * binomial(n + 2, 2) * np ** 2
        complexity_gaussian = np ** w
        complexity = Infinity
        if np > 1 and log2(np) > 1:
            complexity = min(complexity_gaussian, complexity_wiedemann) + (m * q ** (n - k) * nl ** w)
        h = self._h
        return h * log2(q) + log2(complexity)

    def _compute_memory_complexity(self, parameters):
        """
        Return the memory complexity of the algorithm for a given set of parameters

        INPUT:

        - ``parameters`` -- dictionary including the parameters

        TESTS::

            sage: from cryptographic_estimators.MQEstimator.MQAlgorithms.crossbred import Crossbred
            sage: from cryptographic_estimators.MQEstimator.mq_problem import MQProblem
            sage: E = Crossbred(MQProblem(n=10, m=12, q=5))
            sage: E._compute_memory_complexity({'k': 4, 'D': 6, 'd':4})
            12.892542816648552

            sage: E = Crossbred(MQProblem(n=10, m=12, q=5), bit_complexities=False)
            sage: E.memory_complexity()
            19.38013126659691
        """
        k = parameters['k']
        D = parameters['D']
        d = parameters['d']
        ncols_pre_step = self._ncols_in_preprocessing_step(k, D, d)
        ncols_lin_step = self._ncols_in_linearization_step(k, d)
        return log2(ncols_pre_step ** 2 + ncols_lin_step ** 2)

    def _compute_tilde_o_time_complexity(self, parameters):
        """
        Return the Ō time complexity of the algorithm for a given set of parameters

        INPUT:

        - ``parameters`` -- dictionary including the parameters

        TESTS::

            sage: from cryptographic_estimators.MQEstimator.MQAlgorithms.crossbred import Crossbred
            sage: from cryptographic_estimators.MQEstimator.mq_problem import MQProblem
            sage: E = Crossbred(MQProblem(n=10, m=12, q=5))
            sage: E._compute_tilde_o_time_complexity({'k': 4, 'D': 6, 'd':4})
            26.190185554770082

            sage: E = Crossbred(MQProblem(n=10, m=12, q=5), complexity_type=1)
            sage: E.time_complexity()
            19.39681379895914
        """
        k = parameters['k']
        D = parameters['D']
        d = parameters['d']
        np = self._ncols_in_preprocessing_step(k=k, D=D, d=d)
        nl = self._ncols_in_linearization_step(k=k, d=d)
        n, _, q = self.get_reduced_parameters()
        w = self.linear_algebra_constant()
        h = self._h
        return h * log2(q) + log2(np ** 2 + q ** (n - k) * nl ** w)

    def _compute_tilde_o_memory_complexity(self, parameters):
        return self._compute_memory_complexity(parameters)

    def _find_optimal_tilde_o_parameters(self):
        self._find_optimal_parameters()

