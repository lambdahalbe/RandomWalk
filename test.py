from walker import walker
from display import screen
import numpy as np


new_walker = walker(np.array([250, 250, 0]))
new_walker.walk()

new_screen = screen(500, 500, [new_walker], update_steps = 100)
