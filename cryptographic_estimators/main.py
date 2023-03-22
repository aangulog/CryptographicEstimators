
from cryptographic_estimators.PKEstimator import PKEstimator


from cryptographic_estimators.PKEstimator.PKAlgorithms import KMP

A = PKEstimator(n=100, m=50, q=31, ell=2, excluded_algorithms=[KMP])
A.table(precision=3, show_all_parameters=1)

# from cryptographic_estimators.SDFqEstimator import SDFqEstimator
# A = SDFqEstimator(n=100,k=50,w=10,q=5)
# A.table()

# from cryptographic_estimators.SDFqEstimator import SDFqEstimator
# A = SDFqEstimator(961,771,48,31)
# A.table(precision=3, show_all_parameters=1)