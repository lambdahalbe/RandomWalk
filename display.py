import tkinter as tk
from random import choice
from sys import modules
from time import time, sleep


class screen:
    colors = ["red", "green", "blue", "cyan", "magenta"]


    def __init__(self, width, height, walkers, scale=25, update_steps=1, sleep_time=0):
        self.walkers = walkers
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

        for walker in self.walkers:
            walker.init_line(self.cv, self.scale, choice(self.colors))

        self.root.after(200, self.simulate, self.walkers)
        if "idlelib" not in modules:
            self.root.mainloop()


    def __close(self, *ignore):
        print("close function called")
        self.running = False
        self.root.destroy()

    def simulate(self, walkers):
        while self.running:
            sleep(self.sleep_time)
            for walker in walkers:
                for foo in range(self.update_steps):
                    walker.propagate()
                walker.update_line(self.cv, self.scale)
            self.cv.update()
