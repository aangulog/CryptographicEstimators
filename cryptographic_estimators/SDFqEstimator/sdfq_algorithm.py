
from ..helper import ComplexityType
from ..base_algorithm import BaseAlgorithm, optimal_parameter
from .sdfq_problem import SDFqProblem
from .sdfq_helper import _optimize_m4ri
from math import inf, log2


class SDFqAlgorithm(BaseAlgorithm):
    """
    Base class for Syndrome Decoding over FQ algorithms complexity estimator

    INPUT:

    - ``problem`` -- SDFqProblem object including all necessary parameters
    - ``hmp`` -- Indicates if Hashmap is used for list matching, if false sorting is used (default: true)
    """

    def __init__(self, problem: SDFqProblem, **kwargs):
        super(SDFqAlgorithm, self).__init__(problem, **kwargs)
        self._hmap = kwargs.get("hmap", 1)
        self._adjust_radius = kwargs.get("adjust_radius", 10)

    def _time_and_memory_complexity(self, parameters: dict, verbose_information=None):
        """
        Computes time and memory complexity for given parameters
        """
        raise NotImplementedError

    def _compute_time_complexity(self, parameters: dict):
        return self._time_and_memory_complexity(parameters)[0]

    def _compute_memory_complexity(self, parameters: dict):
        return self._time_and_memory_complexity(parameters)[1]

    def _get_verbose_information(self):
        """
        returns a dictionary containing
            {
                CONSTRAINTS,
                PERMUTATIONS,
                TREE,
                GAUSS,
                REPRESENTATIONS,
                LISTS
            }
        """
        verb = dict()
        _ = self._time_and_memory_complexity(self.optimal_parameters(), verbose_information=verb)
        return verb
    
    def __repr__(self):
        pass
