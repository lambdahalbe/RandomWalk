from walker import triangular_walker
from display import screen
import numpy as np


new_walker = triangular_walker(np.array([250, 250]))
for i in range(10):
    new_walker.walk()
print(new_walker.path)
new_screen = screen(500, 500, [new_walker], update_steps = 100)
