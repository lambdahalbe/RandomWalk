import numpy as np
import random
from copy import deepcopy


class walker:


    def __init__(self, start_pos, self_avoiding=False, weighted=True):
        self.steps = 0
        self.pos = start_pos
        self.path = [np.copy(start_pos)]
        self.dim = len(start_pos)
        if self.__class__ == walker:
            self.step_possibilities = [np.zeros(self.dim, dtype=int) for foo in range(2 * self.dim)]
            for i in range(2 * self.dim):
                self.step_possibilities[i][i//2] = 1 - 2 * (i % 2)
        self.self_avoiding = self_avoiding
        if self_avoiding:
            self.position_dic = dict()  # values: not visited -> no value, visited -> 1 (to add options later)
            self.position_dic[tuple(start_pos)] = 1
        self.weighted = weighted
        if weighted:
            self.W = 1


    def possible_steps(self):
        return self.step_possibilities


    def walk(self):
        steps = self.possible_steps()
        if self.self_avoiding:
            steps = self.check_possible(steps)
        if self.weighted:
            self.W *= len(steps)
        step = random.choice(steps)
        self.pos += step
        self.path.append(np.copy(self.pos))
        self.steps += 1
        if self.self_avoiding:
            self.position_dic[tuple(self.pos)] = 1


    def back_propagate(self):
        self.position_dic[tuple(self.pos)] = 0
        self.pos = self.path.pop()
        self.steps -= 1


    def propagate(self):
        self.walk()


    def init_line(self, cv, scale=25, color="black"):
        draw_list = []
        while len(draw_list) < 4:
            for pos in self.path:
                draw_list.append(scale * pos[0])
                draw_list.append(scale * pos[1])
        self.id = cv.create_line(*draw_list, fill=color)


    def update_line(self, cv, scale=25):
        draw_list = []
        for pos in self.path:
            draw_list.append(scale * pos[0])
            draw_list.append(scale * pos[1])
        cv.coords(self.id, *draw_list)


    def check_possible(self, possible_steps):
        allowed = []
        for step in possible_steps:
            position = self.pos + step
            if not self.position_dic.get(tuple(position), False):
                allowed.append(step)
        return allowed


    def copy(self):
        return deepcopy(self)

    
    def atmosphere(self):
        return len(self.check_possible(self.possible_steps()))


class hexagonal_walker(walker):
    even_steps = [np.array((1, 0)), np.array((-1, 0)), np.array((0, 1)), np.array((0, -1)), np.array((1, 1)), np.array((1, -1))]
    odd_steps = [np.array((1, 0)), np.array((-1, 0)), np.array((0, 1)), np.array((0, -1)), np.array((-1, 1)), np.array((-1, -1))]
    vertical_stretch = 3**.5 / 2  # = np.cos(30*(np.pi/180))  # performe calculation only once to increase efficency


    def possible_steps(self):
        if self.pos[1] % 2 == 0:
            return self.even_steps
        else:
            return self.odd_steps
    

    def position_coordinates(self, position):
        if position[1] % 2 == 0:
            x = position[0] + .5
        else:
            x = position[0]
        y = position[1] * self.vertical_stretch
        return np.array((x, y))
 

    def init_line(self, cv, scale=25, color="black"):
        draw_list = []
        while len(draw_list) < 4:  # resolves issue, if only one point to draw
            for pos in self.path:
                coords = self.position_coordinates(pos)
                draw_list.append(scale * coords[0])
                draw_list.append(scale * coords[1])
        self.id = cv.create_line(*draw_list, fill=color)


    def update_line(self, cv, scale=25):
        draw_list = []
        for pos in self.path:
            coords = self.position_coordinates(pos)
            draw_list.append(scale * coords[0])
            draw_list.append(scale * coords[1])
        cv.coords(self.id, *draw_list)


class triangular_walker(walker):
    even_steps = [np.array((1, 0)), np.array((-1, 0)), np.array((0, -1))]
    odd_steps = [np.array((1, 0)), np.array((-1, 0)), np.array((0, 1))]
    dx = 3**.5 / 2  # = np.sin(60 * np.pi / 180)
    dy = .5  # = np.cos(60 * np.pi / 180)


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.odd = (sum(self.pos) % 2 == 0)  # makes change of step possibilities more efficent


    def possible_steps(self):
        if self.odd:
            self.odd = False
            return self.odd_steps
        else:
            self.odd = True
            return self.even_steps


    def back_propagate(self):
        self.odd = not self.odd
        super().back_propagate()


    def position_coordinates(self, position):
        x = position[0] * self.dx
        if position[0] % 2 == 0:
            y = (position[1] // 2) * (2 * self.dy + 1) + ((position[1] + 1) // 2) 
        else:
            y = -self.dy + ((position[1] + 1) // 2) * (2 * self.dy + 1) + (position[1] // 2)
        return np.array((x, y))


    def init_line(self, cv, scale=25, color="black"):
        draw_list = []
        while len(draw_list) < 4:
            for pos in self.path:
                coords = self.position_coordinates(pos)
                draw_list.append(scale * coords[0])
                draw_list.append(scale * coords[1])
        self.id = cv.create_line(*draw_list, fill=color)


    def update_line(self, cv, scale=25):
        draw_list = []
        for pos in self.path:
            coords = self.position_coordinates(pos)
            draw_list.append(scale * coords[0])
            draw_list.append(scale * coords[1])
        cv.coords(self.id, *draw_list)
