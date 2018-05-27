import numpy as np
import random


class walker:


    def __init__(self, start_pos, grid = None):
        self.steps = 0
        self.grid = grid
        self.pos = start_pos
        self.path = [np.copy(start_pos)]
        self.dim = len(start_pos)

    def walk(self):
        direction = np.random.randint(0, self.dim)
        stepsize = random.choice((-1, 1))
        self.pos[direction] += stepsize
        self.path.append(np.copy(self.pos))

    def propagate(self):
        self.walk()

    def init_line(self, cv):
        draw_list = []
        for pos in self.path:
            draw_list.append(pos[0])
            draw_list.append(pos[1])
        self.id = cv.create_line(*draw_list)

    def update_line(self, cv):
        draw_list = []
        for pos in self.path:
            draw_list.append(pos[0])
            draw_list.append(pos[1])
        cv.coords(self.id, *draw_list)
