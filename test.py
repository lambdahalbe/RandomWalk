from walker import triangular_walker
from display import screen
import numpy as np


new_walker = triangular_walker(np.array([20, 20]))
for i in range(10):
    new_walker.walk()
print(new_walker.path)
new_screen = screen(1000, 1000, [new_walker], update_steps = 1)
"hallo franzi"
