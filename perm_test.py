from perm import perm
from walker import hexagonal_walker, triangular_walker, walker
import numpy as np


P = perm(triangular_walker(np.zeros((2), dtype=int), self_avoiding = True, scaling_factor = 2), 800, 8000, "triangular_data.txt", "triangular_meta.txt")

P.run()
