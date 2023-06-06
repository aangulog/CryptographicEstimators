from ..base_problem import BaseProblem


class $$UPPER_CASE_PREFIX$$Problem(BaseProblem):
    """
    Construct an instance of $$UPPER_CASE_PREFIX$$Problem. Contains the parameters to optimize
    over.

    INPUT: 
        - Fill with parameters

    """

    def __init__(self, **kwargs): # Fill with parameters
        super().__init__(**kwargs)

    def to_bitcomplexity_time(self, basic_operations: float):
        """
        Return the bit-complexity corresponding to a certain amount of basic_operations

        INPUT:

        - ``basic_operations`` -- Number of basic operations (logarithmic)

        """
        pass

    def to_bitcomplexity_memory(self, elements_to_store: float):
        """
        Return the memory bit-complexity associated to a given number of elements to store

        INPUT:

        - ``elements_to_store`` -- number of memory operations (logarithmic)

        """
        pass

    def expected_number_solutions(self):
        """
        Return the logarithm of the expected number of existing solutions to the problem

        """
        pass

    def get_parameters(self):
        """
        Return the optimizations parameters
        """
        pass

    def __repr__(self):
        pass
