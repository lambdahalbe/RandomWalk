from random import choice



class perm:


    def __init__(self, walker, max_length, run_threshold, filename, metadata_filename=None):
        self.Weights = [0] * (max_length + 1)  # Weights at Length N
        self.Z = [0] * (max_length + 1)        # Grand Canonical Partion Sum
        self.Copys = [0] * (max_length + 1)    # Number of Copys per Length
        self.dppl = [0] * (max_length + 1)     # DataPoints Per Length
        self.Z[0] = 1                          # Initilize to avoid division by 0
        self.max_length = max_length
        self.walker = walker
        self.c_lower = .3  # TODO find better values
        self.c_upper = 3
        self.run_threshold = run_threshold
        self.filename = filename
        self.file = open(filename, "w")
        self.successful_runs = 0
        self.running = False
        self.meta = False
        if metadata_filename:
            self.meta = True
            self.metadata_file = open(metadata_filename, "w")


    def init_partition_sum(self, aim):
        while self.successful_runs < aim:
            self.step(write=False)
        self.successful_runs = 0
        self.Copys = [0] * (self.max_length + 1)
        self.dppl = [0] * (self.max_length + 1)
        self.Weights = [0] * (self.max_length + 1)
        while self.walker.steps > 0:
            self.walker.back_propagate()
        self.walker.W = 1



    def step(self, write=True):
        if self.walker.steps == self.max_length or self.walker.atmosphere() == 0:
            self.Copys[self.walker.steps] = 0
            if self.walker.steps == self.max_length:
                self.successful_runs += 1
                print("MaxLength reached", self.successful_runs)
                if self.successful_runs >= self.run_threshold:
                    self.running = False
        else:
            W_upper = self.c_upper * self.Z[self.walker.steps] / self.Z[0]
            W_lower = self.c_lower * self.Z[self.walker.steps] / self.Z[0]
            if self.walker.W > W_upper:
                #print("enrichment")
                #self.file.write("enrichment\n")
                self.Copys[self.walker.steps] += 2
                self.walker.W /= 2
                self.Weights[self.walker.steps] = self.walker.W
            elif self.walker.W < W_lower:
                #print("pruning")
                #self.file.write("pruning\n")
                self.walker.W *= 2
                self.Weights[self.walker.steps] = self.walker.W
                if choice([True, False]):
                    self.Copys[self.walker.steps] = 0
                else:
                    self.Copys[self.walker.steps] = 1
            else:
                self.Copys[self.walker.steps] += 1

        
        if self.Copys[self.walker.steps] == 0:
            #self.file.write("Back Propagate\n")
            while self.walker.steps > 0  and self.Copys[self.walker.steps] == 0:
                #self.file.write(str(self.walker.pos))
                self.walker.back_propagate()
                #self.file.write("--->" + str(self.walker.pos) + "\n")
                self.walker.W = self.Weights[self.walker.steps]

        if self.walker.steps == 0 and self.Copys[self.walker.steps] == 0:
            #self.file.write("new_walk\n")
            self.Copys[0] = 1
            self.walker.W = 1
            self.Z[0] += self.walker.W
            self.dppl[0] += 1
            self.writedata()
        
        if self.walker.atmosphere() > 0:
                self.Copys[self.walker.steps] -= 1
                self.walker.walk()
                self.dppl[self.walker.steps] += 1
                self.Weights[self.walker.steps] = self.walker.W
                self.Z[self.walker.steps] += self.walker.W
                if write:
                    self.writedata()

    def run(self):
        self.running = True
        while self.running:
            self.step()
        self.file.close()
        if self.meta:
            self.writemeta()
            self.metadata_file.close()

    def writedata(self):
        line = str(self.walker.steps) + " " + str(self.walker.end_to_end_distance()) +\
                " " + str(self.walker.W) + "\n"
        self.file.write(line)

    def writemeta(self):
        text = "Output Filename: " + self.filename +\
                "\nWalker: " + str(self.walker) + "\nScaling Factor: " + str(self.walker.scaling_factor) +\
                "\nMaxLength: " + str(self.max_length) + "\nRunThreshold: " + str(self.run_threshold) +\
                "\nDatapoints per Length: " + str(self.dppl) + "\nGrand Canonical Partition Sum: " +\
                str(self.Z)
        self.metadata_file.write(text)
