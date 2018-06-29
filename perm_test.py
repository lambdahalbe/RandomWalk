from perm import perm
from walker import hexagonal_walker, triangular_walker, walker
import numpy as np


P = perm(triangular_walker(np.zeros((2), dtype=int), self_avoiding = True, scaling_factor = 2), 500, 1000, metadata_filename="triangular_meta.txt")

P.run()
