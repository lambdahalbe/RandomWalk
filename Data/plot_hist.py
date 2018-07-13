import matplotlib.pylab as plt
import numpy as np
from scipy.optimize import curve_fit


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

def gaussian(x, mu, sigma, A):
    return A * np.exp(-(x - mu)**2 / (2 * sigma**2))


bins = [5, 50, 500]
for i in range(3):

    y, x, patches = plt.hist(data[keys[i]][0], bins=bins[i], weights=data[keys[i]][0], density=True)
    for j in range(len(x) - 1):
        x[i] = 0.5 * (x[j] + x[j + 1])
    x = x[:-1]
    A0 = max(y)
    mu0 = x[-1] / 2
    sigma0 = mu0 / 2
    results = curve_fit(gaussian, x, y, p0 = (mu0, sigma0, A0))
    print("mu", results[0][0])
    print("sigma", results[0][1])
    x = np.linspace(min(x), max(x), 1000)
    if i in [1, 2]:
        plt.plot(x, gaussian(x, *results[0]), "--")
    plt.xlabel("End-To-End-Distance")
    plt.ylabel("Probability")
    plt.show()
