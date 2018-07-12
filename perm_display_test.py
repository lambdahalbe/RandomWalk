from perm_display import *
from perm import *
from walker import *
import numpy as np

ps = perm_screen(1000, 1000, perm(hexagonal_walker(np.array([26, 24]), self_avoiding=True, scaling_factor=4.2),100, 10000), update_steps=1, scale = 20, sleep_time=.0, save = True)

