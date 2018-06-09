from perm import perm
from walker import hexagonal_walker, triangular_walker, walker
import numpy as np


P = perm(triangular_walker(np.zeros((2)), self_avoiding = True), 500)
P.init_partition_sum()
print(P.Z)
