from walker import walker, hexagonal_walker, triangular_walker
from display import screen
import numpy as np


new_walker = triangular_walker(np.array([20, 10]),self_avoiding=True)
for i in range(10):
    new_walker.walk()
print(new_walker.path)
new_screen = screen(2000, 2000, [new_walker], update_steps = 1, scale=50)
