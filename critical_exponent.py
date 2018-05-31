from walker import triangular_walker
import numpy as np

length = 0
runs_per_length = 200

with open("Data/critical_exponent_data.txt", "w") as file:
    while length < 500:
        count = 0
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
