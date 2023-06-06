

from ..base_problem import BaseProblem
from math import comb, log2
from .sd_constants import *


class SDProblem(BaseProblem):
    """
    Construct an instance of the Syndrome Decoding Problem

    INPUT:

    - ``n`` -- code length
    - ``k`` -- code dimension
    - ``w`` -- error weight
    - ``nsolutions`` -- number of (expected) solutions of the problem in logarithmic scale
    - ``memory_bound`` -- maximum allowed memory to use for solving the problem

    """

    def __init__(self, n: int, k: int, w: int, **kwargs):
        super().__init__(**kwargs)
        if k > n:
            raise ValueError("k must be smaller or equal to n")
        if w > n - k:
            raise ValueError("w must be smaller or equal to n-k")
        if w <= 0 or k <= 0:
            raise ValueError("w and k must be at least 1")
        self.parameters[SD_CODE_LENGTH] = n
        self.parameters[SD_CODE_DIMENSION] = k
        self.parameters[SD_ERROR_WEIGHT] = w

        self.nsolutions = kwargs.get("nsolutions", max(
            self.expected_number_solutions(), 0))

    def to_bitcomplexity_time(self, basic_operations: float):
        """
        Returns the bit-complexity corresponding to basic_operations field additions

        INPUT:

        - ``basic_operations`` -- Number of field additions (logarithmic)

        """
        n = self.parameters[SD_CODE_LENGTH]
        q = 2
        return log2(log2(q)) + log2(n) + basic_operations

    def to_bitcomplexity_memory(self, elements_to_store: float):
        """
        Returns the memory bit-complexity associated to a given number of elements to store

        INPUT:

        - ``elements_to_store`` -- number of memory operations (logarithmic)

        """
        return self.to_bitcomplexity_time(elements_to_store)

    def expected_number_solutions(self):
        """
        Returns the logarithm of the expected number of existing solutions to the problem

        """
        n, k, w = self.get_parameters()
        return log2(comb(n, w)) - (n - k)

    def __repr__(self):
        """
        """
        n, k, w  = self.get_parameters()
        rep = "syndrome decoding problem with (n,k,w) = " \
              + "(" + str(n) + "," + str(k) + "," + str(w) + ") over Finite Field of size 2"
        return rep

    def get_parameters(self):
        """
        Returns the ISD paramters n, k, w
        """
        n = self.parameters[SD_CODE_LENGTH]
        k = self.parameters[SD_CODE_DIMENSION]
        w = self.parameters[SD_ERROR_WEIGHT]
        return n, k, w
