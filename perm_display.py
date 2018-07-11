import tkinter as tk
from random import choice
from sys import modules
from time import time, sleep


class perm_screen:
    colors = ["red", "green", "blue", "cyan", "magenta"]


    def __init__(self, width, height, perm, scale=25, update_steps=1, sleep_time=0):
        self.perm = perm
        self.scale = scale
        self.update_steps = update_steps
        self.sleep_time = sleep_time
        self.root = tk.Tk()
        self.cv = tk.Canvas(self.root, width=width, height=height)
        self.cv.create_rectangle(0, 0, width, height, fill="pink")
        self.cv.pack()

        self.root.bind('<Escape>', self.__close)
        self.root.protocol('WM_DELETE_WINDOW', self.__close)

        self.running = True

        perm.walker.init_line(self.cv, self.scale, "black")

        self.root.after(200, self.simulate)
        if "idlelib" not in modules:
            self.root.mainloop()


    def __close(self, *ignore):
        print("close function called")
        self.running = False
        self.root.destroy()

    def simulate(self):
        while self.running:
            sleep(self.sleep_time)
            for foo in range(self.update_steps):
                self.perm.step()
            dots = []
            for i in range(self.perm.walker.steps):
                if self.perm.Copys[i] != 0:
                    x, y  = self.perm.walker.position_coordinates(self.perm.walker.path[i])
                    s = self.scale
                    r = 2 / 25
                    dots.append(self.cv.create_oval(s * (x-r), s * (y-r), s * (x+r), s * (y+r), fill = "black"))
            print(dots)
            self.perm.walker.update_line(self.cv, self.scale)
            self.cv.update()
            for dot in dots:
                self.cv.delete(dot)
