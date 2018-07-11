from perm_display import *
from perm import *
from walker import *
import numpy as np

ps = perm_screen(1000, 1000, perm(triangular_walker(np.array([100, 70]), self_avoiding=True),2000, 100), scale = 5, sleep_time=.03)

