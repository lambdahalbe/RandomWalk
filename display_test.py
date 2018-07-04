from walker import walker, hexagonal_walker, triangular_walker
from display import screen
import numpy as np

walkers = [triangular_walker(np.array([30, 10]), self_avoiding=False) for i in range(500)]
new_screen = screen(2000, 2000, walkers, update_steps = 1, scale=30, sleep_time=.0)
