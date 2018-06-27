from perm import perm
from walker import hexagonal_walker, triangular_walker, walker
import numpy as np


P = perm(triangular_walker(np.zeros((2), dtype=int), self_avoiding = True), 500, 1000000000, "blub.txt")

P.init_partition_sum()
P.walker.scaling_factor = P.Z[-1]**(1/(len(P.Z)-1))
for i in range(len(P.Z)):
    P.Z[i] /= P.walker.scaling_factor**i
print(len(P.Z))
print(P.Z)
print(P.walker.scaling_factor)
P.run()
