import numpy as np
import random


class walker:


    def __init__(self, start_pos, self_avoiding=False):
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


    def walk(self):
        if self.self_avoiding:
            step = random.choice(self.check_possible(self.step_possibilities))
        else:
            step = random.choice(self.step_possibilities)
        self.pos += step
        self.path.append(np.copy(self.pos))
        self.steps += 1
        if self.self_avoiding:
            self.position_dic[tuple(self.pos)] = 1


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


class hexagonal_walker(walker):
    even_steps = [np.array((1, 0)), np.array((-1, 0)), np.array((0, 1)), np.array((0, -1)), np.array((1, 1)), np.array((1, -1))]
    odd_steps = [np.array((1, 0)), np.array((-1, 0)), np.array((0, 1)), np.array((0, -1)), np.array((-1, 1)), np.array((-1, -1))]
    vertical_stretch = 3**.5 / 2  # = np.cos(30*(np.pi/180))  # performe calculation only once to increase efficency
    
    
    def walk(self):
        if self.self_avoiding:
            if self.pos[1] % 2 == 0:
                step = random.choice(self.check_possible(self.even_steps))
            else:
                step = random.choice(self.check_possible(self.odd_steps))
        else:
            if self.pos[1] % 2 == 0:
                step = random.choice(self.even_steps)
            else:
                step = random.choice(self.odd_steps)

        self.pos += step
        self.path.append(np.copy(self.pos))
        if self.self_avoiding:
            self.position_dic[tuple(self.pos)] = 1
        self.steps += 1


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


    def walk(self):
        if self.self_avoiding:
            if sum(self.pos) % 2 == 0:
                step = random.choice(self.check_possible(self.odd_steps))
            else:
                step = random.choice(self.check_possible(self.even_steps))
        else:            
            if sum(self.pos) % 2 == 0:
                step = random.choice(self.odd_steps)
            else:
                step = random.choice(self.even_steps)

        self.pos += step
        self.path.append(np.copy(self.pos))
        if self.self_avoiding:
            self.position_dic[tuple(self.pos)] = 1        
        self.steps += 1


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
