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
        step = random.choice((-1, 1))
        self.pos[direction] += step
        self.path.append(np.copy(self.pos))
        self.steps += 1

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

    def check_possible(self, possible_steps):
        allowed = []
        for step in possible_steps:
            position = self.pos + step
            if not grid[position[0]][position[1]]:
                allowed.append(step)
        return allowed


class hexagonal_walker(walker):
    even_steps = [np.array((1, 0)), np.array((-1, 0)), np.array((0, 1)), np.array((0, -1)), np.array((1, 1)), np.array((1, -1))]
    odd_steps = [np.array((1, 0)), np.array((-1, 0)), np.array((0, 1)), np.array((0, -1)), np.array((-1, 1)), np.array((-1, -1))]
    
    
    def walk(self):
        if self.pos[1] % 2 == 0:
            step = random.choice(self.even_steps)
        else:
            step = random.choice(self.odd_steps)

        self.pos += step
        self.path.append(np.copy(self.pos))
        self.steps += 1
    
    def init_line(self, cv, scale=25):
        #TODO see update line
        draw_list = []
        for pos in self.path:
            if pos[1] % 2 == 0:
                draw_list.append(scale * (pos[0] + .5))
            else:
                draw_list.append(scale * pos[0])
            draw_list.append(scale * np.cos(30*(np.pi/180))* pos[1])
        self.id = cv.create_line(*draw_list)

    def update_line(self, cv, scale=25):
        #TODO no hard-coded scaling factor!
        draw_list = []
        for pos in self.path:
            if pos[1] % 2 == 0:
                draw_list.append(scale * (pos[0] + .5))
            else:
                draw_list.append(scale * pos[0])
            draw_list.append(scale * pos[1] * np.cos(30*(np.pi/180)))
        cv.coords(self.id, *draw_list)
