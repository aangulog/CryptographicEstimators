

from enum import Enum

SDFQ_CODE_LENGTH = "code length"
SDFQ_CODE_DIMENSION = "code dimension"
SDFQ_ERROR_WEIGHT = "error weight"
SDFQ_ERROR_FIELD_SIZE = "field size"


class VerboseInformation(Enum):
    """
    """
    CONSTRAINTS = "constraints"
    PERMUTATIONS = "permutations"
    TREE = "tree"
    GAUSS = "gauss"
    REPRESENTATIONS = "representation"
    LISTS = "lists"
