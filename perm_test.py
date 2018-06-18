from perm import perm
from walker import hexagonal_walker, triangular_walker, walker
import numpy as np


P = perm(triangular_walker(np.zeros((2), dtype=int), self_avoiding = True), 10, 1000)
P.run()
