from random import choice



class perm:


    def __init__(self, walker, max_length, end_weight, filename):
        self.Weights = []  # Weights at length N
        self.Z = []  # grand canonical partion sum
        self.Copys = []
        for i in range(max_length + 1):
            self.Copys.append(0)
            self.Z.append(0)
            self.Weights.append(0)
        self.Z[0] = 1
        self.max_length = max_length
        self.walker = walker
        self.c_lower = .3  # TODO find better values
        self.c_upper = 2.5
        self.end_weight = end_weight
        self.file = open(filename, "w")


    def init_partition_sum(self):
        while True:
            try:
                self.Z = []
                new_walker = self.walker.copy()
                for i in range(self.max_length):
                    self.Z.append(new_walker.W)
                    new_walker.walk()
                break
            except IndexError:
                continue

    def step(self):
        if self.walker.steps == self.max_length or self.walker.atmosphere() == 0:
            self.Copys[self.walker.steps] = 0
        else:
            W_upper = self.c_upper * self.Z[self.walker.steps] / self.Z[0]
            W_lower = self.c_lower * self.Z[self.walker.steps] / self.Z[0]
            if self.walker.W > W_upper:
                print("enrichment")
                self.file.write("enrichment\n")
                self.Copys[self.walker.steps] += 2
                self.walker.W /= 2
                self.Weights[self.walker.steps] = self.walker.W
            elif self.walker.W < W_lower:
                print("pruning")
                self.file.write("pruning\n")
                self.walker.W *= 2
                self.Weights[self.walker.steps] = self.walker.W
                if choice([True, False]):
                    self.Copys[self.walker.steps] = 0
                else:
                    self.Copys[self.walker.steps] = 1
            else:
                self.Copys[self.walker.steps] += 1

        
        if self.Copys[self.walker.steps] == 0:
            self.file.write("Back Propagate\n")
            while self.walker.steps > 0  and self.Copys[self.walker.steps] == 0:
                self.file.write(str(self.walker.pos))
                self.walker.back_propagate()
                self.file.write("--->" + str(self.walker.pos) + "\n")
                self.walker.W = self.Weights[self.walker.steps]

        if self.walker.steps == 0 and self.Copys[self.walker.steps] == 0:
            self.file.write("new_walk\n")
            self.Copys[0] = 1
            self.walker.W = 1
            self.Z[0] += self.walker.W
            self.writedata()
        
        if self.walker.atmosphere() > 0:
                self.Copys[self.walker.steps] -= 1
                self.walker.walk()
                self.Weights[self.walker.steps] = self.walker.W
                self.Z[self.walker.steps] += self.walker.W
                self.writedata()

    def run(self):
        while self.Z[-1] < self.end_weight:
            self.step()
        self.file.close()

    def writedata(self):
        line = str(self.walker.steps) + " " + str(self.walker.end_to_end_distance()) +\
                " " + str(self.walker.W) + "\n"
        self.file.write(line)
