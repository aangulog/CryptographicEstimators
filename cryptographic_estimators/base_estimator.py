# ****************************************************************************
# Copyright 2023 Technology Innovation Institute
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
# ****************************************************************************


from concurrent import futures
import time
from multiprocessing import Manager
from multiprocessing.managers import DictProxy
from math import isinf
from typing import Union, Callable
from .helper import ComplexityType
from .base_constants import BASE_TILDEO_ESTIMATE, BASE_ADDITIONALO, BASE_BIT_COMPLEXITIES, BASE_ESTIMATEO, BASE_EXCLUDED_ALGORITHMS, BASE_MEMORY, BASE_PARAMETERS, BASE_QUANTUMO, BASE_TIME
from .base_algorithm import BaseAlgorithm
from .estimation_renderer import EstimationRenderer


class BaseEstimator(object):
    """
    Construct an instance of BaseEstimator

    INPUT:

    - ``alg`` -- specialized algorithm class (subclass of BaseAlgorithm)
    - ``prob`` -- object of any subclass of BaseProblem
    - ``excluded_algorithms`` -- a list/tuple of excluded algorithms (default: None)
    - ``memory_access`` -- specifies the memory access cost model (default: 0, choices: 0 - constant, 1 - logarithmic, 2 - square-root, 3 - cube-root or deploy custom function which takes as input the logarithm of the total memory usage)
    - ``complexity_type`` -- complexity type to consider (0: estimate, 1: tilde O complexity, default 0)
    - ``bit_complexities`` -- state complexity as bit rather than field operations (default 1, only relevant for complexity_type 0)
    - ``include_tildeo`` -- specifies if tildeO estimation should be included in the outputs (default 0: no tildeO esimation)
    - ``include_quantum`` -- specifies if quantum estimation should be included in the outputs (default 0: no quyantum esimation)

    """
    excluded_algorithms_by_default = []

    def __init__(self, base_algorithm_subclass, problem_instance, **kwargs):
        excluded_algorithms = kwargs.get(BASE_EXCLUDED_ALGORITHMS, [])

        if (self._are_all_excluded_algorithms_valid_subclasses(base_algorithm_subclass, excluded_algorithms)):
            raise TypeError(
                f"All excluded algorithms must be a subclass of {base_algorithm_subclass.__name__}")

        self.estimates = {}
        self.problem = problem_instance
        # self._algorithms = []
        self._algorithms = self._get_instantiated_algorithms(
            base_algorithm_subclass, excluded_algorithms)
        # Why?
        self._bit_complexities = kwargs.get(BASE_BIT_COMPLEXITIES, 1)
        self.bit_complexities = self._bit_complexities
        ##
        self.include_tildeo = kwargs.get("include_tildeo", False)
        self.include_quantum = kwargs.get("include_quantum", False)

    def _are_all_excluded_algorithms_valid_subclasses(self, algorithm_subclass, excluded_algorithms):
        return any(not issubclass(Algorithm, algorithm_subclass) for Algorithm in excluded_algorithms)

    def _get_instantiated_algorithms(self, base_algorithm_subclass, excluded_algorithms, **kwargs):
        included_algorithms = (Algorithm for Algorithm in base_algorithm_subclass.__subclasses__(
        ) if Algorithm not in excluded_algorithms)
        instantiated_algorithms = []
        for algorithm_subclass in included_algorithms:
            try:
                algorithm = algorithm_subclass(self.problem, **kwargs)
            except (ValueError, TypeError):
                # Why? Do we want to notify user that some algorithm could not be instantiated?
                continue

            # self._algorithms.append(algorithm)
            instantiated_algorithms.append(algorithm)
            # This adds to the BaseEstimator instance a new member with the name of the algorithm
            # So this makes self.algorithm. accesible
            # This is weird because we already have a list of algorithms
            setattr(self, algorithm.__module__.split('.')[-1], algorithm)
        return instantiated_algorithms

    @property
    def memory_access(self):
        """
        Returns a list of memory_access attributes of included algorithms

        """
        return [i.memory_access for i in self._algorithms]

    @memory_access.setter
    def memory_access(self, new_memory_access: Union[int, Callable[[float], float]]):
        """
        Sets the memory_access attribute of all included algorithms

        INPUT:

        - ``new_memory_access`` -- new memory access value. Either (0 - constant, 1 - logarithmic, 2 - square-root, 3 - cube-root or deploy custom function which takes as input the logarithm of the total memory usage)

        """
        for i in self._algorithms:
            i.memory_access = new_memory_access

    @property
    def complexity_type(self):
        """
        Returns a list of complexity_type attributes of included algorithms

        """
        return [i.complexity_type for i in self._algorithms]

    @complexity_type.setter
    def complexity_type(self, new_complexity_type: ComplexityType):
        """
        Sets the complexity_type attribute of all included algorithms

        INPUT:

        - ``new_complexity_type`` -- new complexy_type value. Either (0: estimate, 1: tilde O complexity)

        """
        for i in self._algorithms:
            i.complexity_type = new_complexity_type

    @property
    def bit_complexities(self):
        """
        Returns a list of bit_complexities attributes of included algorithms

        """
        return [i.bit_complexities for i in self._algorithms]

    @bit_complexities.setter
    def bit_complexities(self, new_bit_complexities: int):
        """
        Sets the bit_complexities attribute of all included algorithms

        INPUT:

        - ``new_bit_complexities`` -- new bit_complexities value.

        """
        if self._bit_complexities != new_bit_complexities:
            self._bit_complexities = new_bit_complexities
            self.reset()
            for i in self._algorithms:
                i.bit_complexities = new_bit_complexities

    def algorithms(self):
        """
        Return a list of considered algorithms

        """
        return self._algorithms

    def algorithm_names(self):
        """
        Return a list of the name of considered algorithms

        """
        return [algorithm.__class__.__name__ for algorithm in self.algorithms()]

    def nalgorithms(self):
        """
        Return the number of considered algorithms

        """
        return len(self.algorithms())

    def _add_tilde_o_complexity(self, algorithm: BaseAlgorithm):
        """
        runs the tilde O complexity analysis for the given `algorithm`

        INPUT:

        - ``algorithm`` -- Algorithm to run.

        """
        est = self.estimates
        name = algorithm.__class__.__name__
        algorithm.complexity_type = ComplexityType.TILDEO.value
        est[name][BASE_TILDEO_ESTIMATE] = {}

        try:
            est[name][BASE_TILDEO_ESTIMATE][BASE_TIME] = algorithm.time_complexity()
        except NotImplementedError:
            est[name][BASE_TILDEO_ESTIMATE][BASE_TIME] = "--"
        try:
            est[name][BASE_TILDEO_ESTIMATE][BASE_MEMORY] = algorithm.memory_complexity()
        except NotImplementedError:
            est[name][BASE_TILDEO_ESTIMATE][BASE_MEMORY] = "--"
        try:
            est[name][BASE_TILDEO_ESTIMATE][BASE_PARAMETERS] = algorithm.get_optimal_parameters_dict()
        except NotImplementedError:
            est[name][BASE_TILDEO_ESTIMATE][BASE_PARAMETERS] = "--"

    def _add_quantum_complexity(self, algorithm: BaseAlgorithm):
        """
        runs the quantum time analysis for the given `algorithm`

        INPUT:

        - ``algorithm`` -- Algorithm to run.

        """
        est = self.estimates
        name = algorithm.__class__.__name__
        try:
            est[name][BASE_QUANTUMO] = {}
            est[name][BASE_QUANTUMO][BASE_TIME] = algorithm.quantum_time_complexity()
        except NotImplementedError:
            est[name][BASE_QUANTUMO][BASE_TIME] = "--"

    def _add_estimate(self, algorithm: BaseAlgorithm):
        """
        runs the bit security analysis for the given `algorithm`

        INPUT:

        - ``algorithm`` -- Algorithm to run.

        """
        est = self.estimates
        name = algorithm.__class__.__name__
        algorithm.complexity_type = ComplexityType.ESTIMATE.value
        est[name][BASE_ESTIMATEO] = {}

        est[name][BASE_ESTIMATEO][BASE_TIME] = algorithm.time_complexity() if not isinf(
            algorithm.time_complexity()) else '--'

        est[name][BASE_ESTIMATEO][BASE_MEMORY] = algorithm.memory_complexity() if not isinf(
            algorithm.memory_complexity()) else '--'

        est[name][BASE_ESTIMATEO][BASE_PARAMETERS] = algorithm.get_optimal_parameters_dict()

        est[name][BASE_ADDITIONALO] = algorithm._get_verbose_information(
        ) if not isinf(algorithm.time_complexity()) else {}

    def estimate(self, **kwargs):
        """
        Returns dictionary describing the complexity of each algorithm and its optimal parameters

        """
        logger = kwargs.get("logger", None)
        start_time = time.time()

        if not self.estimates:
            self.estimates = dict()

        for index, algorithm in enumerate(self.algorithms()):
            name = algorithm.__class__.__name__
            if name not in self.estimates:
                self.estimates[name] = {}

            # used only in the GUI
            if logger:
                logger(
                    f"[{str(index + 1)}/{str(self.nalgorithms())}] - Processing algorithm: '{name}'")

            # if self.include_tildeo and BASE_TILDEO_ESTIMATE not in self.estimates[name]:
            #     self._add_tilde_o_complexity(algorithm)

            # if self.include_quantum and BASE_QUANTUMO not in self.estimates[name]:
            #     self._add_quantum_complexity(algorithm)

            if BASE_ESTIMATEO not in self.estimates[name]:
                self._add_estimate(algorithm)

        end_time = time.time()
        print(f"Total time: {end_time - start_time}")
        return self.estimates

    def table(self, show_quantum_complexity=False, show_tilde_o_time=False, show_all_parameters=False, precision=1, truncate=False):
        """
        Print table describing the complexity of each algorithm and its optimal parameters

        INPUT:

        - ``show_quantum_complexity`` -- show quantum time complexity (default: false)
        - ``show_tilde_o_time`` -- show Ō time complexity (default: false)
        - ``show_all_parameters`` -- show all optimization parameters (default: false)
        - ``precision`` -- number of decimal digits output (default: 1)
        - ``truncate`` -- truncate rather than round the output (default: false)

        """
        self.include_tildeo = show_tilde_o_time
        self.include_quantum = show_quantum_complexity
        estimate = self.estimate()

        if estimate == {}:
            raise ValueError(
                "No algorithm associated with this estimator or applicable to this problem instance.")

        else:
            renderer = EstimationRenderer(
                show_quantum_complexity, show_tilde_o_time, show_all_parameters, precision, truncate
            )
            renderer.as_table(estimate)

    def fastest_algorithm(self, use_tilde_o_time=False):
        """
         Return the algorithm with the smallest time complexity

         INPUT:

         - ``use_tilde_o_time`` -- use Ō time complexity, i.e., ignore polynomial factors (default: False)
         """
        if use_tilde_o_time:
            self.complexity_type = ComplexityType.TILDEO.value

        def key(algorithm):
            return algorithm.time_complexity()

        return min(self.algorithms(), key=key)

    def reset(self):
        """
        Resets the internal states of the estimator and all included algorithms

        """

        self.estimates = {}
        for i in self.algorithms():
            i.reset()

    def multithread_estimate(self, **kwargs):
        """
        Returns dictionary describing the complexity of each algorithm and its optimal parameters

        """
        start_time = time.time()
        if not self.estimates:
            self.estimates = dict()

        with futures.ThreadPoolExecutor() as executor:
            for index, algorithm in enumerate(self.algorithms()):
                name = algorithm.__class__.__name__
                if name not in self.estimates:
                    self.estimates[name] = {}

                print(
                    f"[{str(index + 1)}/{str(self.nalgorithms())}] - Processing algorithm: '{name}'")

                if BASE_ESTIMATEO not in self.estimates[name]:
                    executor.submit(self._add_estimate, algorithm)
        end_time = time.time()
        print(f"Total time: {end_time - start_time}")
        return self.estimates

    def multiprocess_estimate(self, **kwargs):
        """
        Returns dictionary describing the complexity of each algorithm and its optimal parameters

        """
        start_time = time.time()
        if not self.estimates:
            self.estimates = dict()

        futurelist = []
        manager = Manager()
        shared_estimates = manager.dict()

        with futures.ProcessPoolExecutor() as executor:
            for index, algorithm in enumerate(self.algorithms()):
                name = algorithm.__class__.__name__
                if name not in shared_estimates:
                    shared_estimates[name] = {}

                print(
                    f"[{str(index + 1)}/{str(self.nalgorithms())}] - Processing algorithm: '{name}'")

                if BASE_ESTIMATEO not in shared_estimates[name]:
                    future = executor.submit(
                        self.shared_add_estimate, algorithm, shared_estimates)
                    futurelist.append(future)

            # Wait for all futures to complete
            futures.wait(futurelist)
            for future in futurelist:
                result = future.result()
                if isinstance(result, Exception):
                    raise result

        self.estimates.update(shared_estimates)
        end_time = time.time()
        print(f"Total time: {end_time - start_time}")
        return self.estimates

    def shared_add_estimate(self, algorithm: BaseAlgorithm, shared_dict: DictProxy):
        """
        runs the bit security analysis for the given `algorithm`

        INPUT:

        - ``algorithm`` -- Algorithm to run.

        """
        name = algorithm.__class__.__name__
        algorithm.complexity_type = ComplexityType.ESTIMATE.value
        time_complexity = algorithm.time_complexity()
        memory_complexity = algorithm.memory_complexity()
        time_complexity_value = time_complexity if not isinf(
            time_complexity) else '--'
        memory_complexity_value = memory_complexity if not isinf(
            memory_complexity) else '--'
        verbose_information = algorithm._get_verbose_information(
        ) if not isinf(time_complexity) else {}
        optimal_parameters = algorithm.get_optimal_parameters_dict_with_primitive_types()

        shared_dict[name] = {
            BASE_ESTIMATEO: {
                BASE_TIME: time_complexity_value,
                BASE_MEMORY: memory_complexity_value,
                BASE_PARAMETERS: optimal_parameters
            },
            BASE_ADDITIONALO: verbose_information
        }
