from walker import triangular_walker
import numpy as np
import sys

if len(sys.argv) < 2:
    exit()

length = 430
runs_per_length = 1

with open(sys.argv[1], "w") as file:
    while length < 500:
        count = 0
        print(length)
        while count < runs_per_length:
            walker = triangular_walker(np.zeros((2)), self_avoiding=True)
            try:
                for foo in range(length):
                    walker.walk()
            except:
                continue
            file.write(str(length) + " " + str(np.linalg.norm(walker.position_coordinates(walker.pos))) + "\n")
            count += 1
        length += 1
