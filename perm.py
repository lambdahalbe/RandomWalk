

class perm:


    def __init__(self, walker, max_length):
        self.Weights = []  # Weights at length N
        self.Z = []  # grand canonical partion sum
        self.Copys = []
        for i in range(max_length + 1):
            self.Copys.append(0)
        self.Copys[0] = 1
        self.max_length = max_length
        self.walker = walker


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
        if self.walker.steps == self.max_length or len(self.walker.atmosphere) == 0:
            self.Copys[self.walker.steps] = 0
        else:
            pass  # TODO pruning/enrichment
        
        if self.Copys[self.walker.steps] == 0:
            while self.walker.steps > 0  and self.Copys[self.walker.steps] == 0:
                self.walker.back_propagate()
                self.walker.W = self.Weights[self.walker.steps]

        if self.walker.steps == 0 and self.Copys[self.walker.steps] == 0:
            self.Copys[0] = 1
            self.walker.W = 1
        else:
            if self.walker.atmosphere() > 0:
                self.Copys[self.walker.steps] -= 1
                self.walker.walk()
                self.Weights[self.walker.steps] =self.walker.W
                self.Z[self.walker.steps] += self.walker.W

