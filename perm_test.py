from perm import perm
from walker import hexagonal_walker, triangular_walker, walker
import numpy as np


P = perm(hexagonal_walker(self_avoiding = True, scaling_factor = 4.2), 500, 1000, metadata_filename="hexagonal_meta.txt")

P.run()
