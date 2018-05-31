from walker import walker, hexagonal_walker, triangular_walker
from display import screen
import numpy as np

walkers = [triangular_walker(np.array([20, 10]), self_avoiding=True) for i in range(10)]
new_screen = screen(2000, 2000, walkers, update_steps = 1, scale=50, sleep_time=.3)
