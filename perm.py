from random import choice



class perm:


    def __init__(self, walker, max_length, end_weight):
        self.Weights = []  # Weights at length N
        self.Z = []  # grand canonical partion sum
        self.Copys = []
        for i in range(max_length + 1):
            self.Copys.append(0)
            self.Z.append(0)
            self.Weights.append(0)
        self.Copys[0] = 0
        self.Z[0] = 1
        self.max_length = max_length
        self.walker = walker
        self.c_lower = .3  # TODO find better values
        self.c_upper = 3
        self.end_weight = end_weight


    def init_partition_sum(self):
        while True:
            try:
                self.Z = []
                new_walker = self.walker.copy()
                for i in range(self.max_length):
                    self.Z.append(new_walker.W)
                    new_walker.walk()
                print("Initilization of Partition Sum finished")
                break
            except IndexError:
                continue

    def step(self):
        print(self.walker.atmosphere())
        if self.walker.steps == self.max_length or self.walker.atmosphere() == 0:
            print("Reached max_length or dead end")
            self.Copys[self.walker.steps] = 0
        else:
            W_upper = self.c_upper * self.Z[self.walker.steps] / self.Z[0]
            W_lower = self.c_lower * self.Z[self.walker.steps] / self.Z[0]
            print(W_lower, self.walker.W, W_upper)
            if self.walker.W > W_upper:
                print("Enriched")
                self.Copys[self.walker.steps] += 2
                self.walker.W /= 2
                self.Weights[self.walker.stpes] = self.walker.W
            elif self.walker.W < W_lower:
                print("Prune attempt")
                self.walker.W *= 2
                self.Weights[self.walker.steps] = self.walker.W
                if choice([True, False]):
                    print("Pruning accepted")
                    self.Copys[self.walker.steps] = 0
                else:
                    self.Copys[self.walker.steps] = 1
            else:
                print("No Enrichment/Pruning")
                self.Copys[self.walker.steps] += 1

        
        if self.Copys[self.walker.steps] == 0:
            while self.walker.steps > 0  and self.Copys[self.walker.steps] == 0:
                print("Shrinking to length " + str(self.walker.steps))
                self.walker.back_propagate()
                self.walker.W = self.Weights[self.walker.steps]

        if self.walker.steps == 0 and self.Copys[self.walker.steps] == 0:
            print("Start new run")
            self.Copys[0] = 1
            self.walker.W = 1
            self.Z[0] += self.walker.W
        
        if self.walker.atmosphere() > 0:
                print("Step at length " + str(self.walker.steps))
                self.Copys[self.walker.steps] -= 1
                self.walker.walk()
                self.Weights[self.walker.steps] = self.walker.W
                self.Z[self.walker.steps] += self.walker.W

    def run(self):
        while self.Z[-1] < self.end_weight:
            print("Z:", self.Z)
            print("Copys:", self.Copys)
            self.step()
