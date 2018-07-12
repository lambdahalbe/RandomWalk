from perm_display import *
from perm import *
from walker import *
import numpy as np


p = perm(triangular_walker(np.array([165, 97]), self_avoiding=True, scaling_factor=1.85),1000, 10000)
for i in range(len(p.Z)):
    p.Z[i] = 1

ps = perm_screen(1500, 1500, p, update_steps=30, scale = 5, sleep_time=.0, save = True)

