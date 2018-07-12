import matplotlib.pylab as plt
import numpy as np

data = {}
keys = [10, 100, 1000]
for i in keys:
    data[i] = [[], []]

with open("triangular_hist_data.txt", "r") as f:
    for line in f:
        steps, dist, weight = line.split()
        steps = int(steps)
        dist = float(dist)
        weight = float(weight)
        data[steps][0].append(dist)
        data[steps][1].append(weight)

for i in keys:
    data[i][0] = np.array(data[i][0])
    data[i][1] = np.array(data[i][1])


bins = [5, 50, 500]
for i in range(3):

    plt.hist(data[keys[i]][0], bins=bins[i], weights=data[keys[i]][0], density=True)
    plt.xlabel("End-To-End-Distance")
    plt.ylabel("Probability")
    plt.show()
