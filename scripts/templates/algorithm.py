from ..base_algorithm import BaseAlgorithm
from .$$lower_case_prefix$$_problem import $$UPPER_CASE_PREFIX$$Problem


class $$UPPER_CASE_PREFIX$$Algorithm(BaseAlgorithm):
    def __init__(self, problem: $$UPPER_CASE_PREFIX$$Problem, **kwargs):
        """
        Base class for $$UPPER_CASE_PREFIX$$ algorithms complexity estimator

        INPUT:

        - ``problem`` -- $$UPPER_CASE_PREFIX$$Problem object including all necessary parameters

        """
        self._name = "sample_name"
        super($$UPPER_CASE_PREFIX$$Algorithm, self).__init__(problem, **kwargs)

    def __repr__(self):
        """
        NOTE: self._name must be instanciated via the child class
        """
        pass
