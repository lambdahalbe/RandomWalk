from walker import triangular_walker
import numpy as np
import sys

if len(sys.argv) < 2:
    exit()

start_length = 0
end_length = 500
runs_per_length= 1000

with open(sys.argv[1], "w") as file:
    while start_length < end_length:
        count = 0
        failed = 0
        weighted_size = 0
        print("length:", start_length)
        while count < runs_per_length:
            walker = triangular_walker(np.zeros((2)), self_avoiding = True)
            try:
                for foo in range(start_length):
                    walker.walk()
            except IndexError:
                failed += 1
            finally:
                count += 1
        print("failed:", failed)
        file.write(str(start_length) + " " + str(failed) + "\n")
        start_length += 1
