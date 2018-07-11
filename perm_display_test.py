from perm_display import *
from perm import *
from walker import *
import numpy as np

ps = perm_screen(1000, 1000, perm(triangular_walker(np.array([26, 16]), self_avoiding=True, scaling_factor=1.85),100, 10000), update_steps=1, scale = 20, sleep_time=.0, save = True)

