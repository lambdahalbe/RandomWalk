from walker import walker, hexagonal_walker, triangular_walker
from display import screen
import numpy as np

walkers = [triangular_walker(np.array([20, 10]), self_avoiding=False) for i in range(100)]
new_screen = screen(2000, 2000, walkers, update_steps = 100, scale=50, sleep_time=.0)
