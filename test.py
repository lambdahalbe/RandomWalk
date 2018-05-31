from walker import walker, hexagonal_walker
from display import screen
import numpy as np


new_walker1 = walker(np.array((10,10)))
new_walker2 = hexagonal_walker(np.array([30, 30]))
new_walker3 = walker(np.array((25,15)), self_avoiding=True)
new_walker4 = hexagonal_walker(np.array((15,25)), self_avoiding=True)

new_screen = screen(1000, 1000, [new_walker4], update_steps = 1, sleep_time = .2, scale=40)
