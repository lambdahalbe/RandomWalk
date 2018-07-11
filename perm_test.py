from perm import perm
from walker import hexagonal_walker, triangular_walker, walker
import numpy as np


P = perm(triangular_walker(self_avoiding = True, scaling_factor = 1.85), 1000, 100000, filename="triangular_hist_data.txt")

P.run()
