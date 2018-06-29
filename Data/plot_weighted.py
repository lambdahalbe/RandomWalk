import matplotlib.pylab as plt
import numpy as np
from scipy.optimize import curve_fit

filename = "triangular_data_old.txt"
maxLength = 2000
lFB = 200  # lowerFitBoundary

data = []
for i in range(maxLength + 1):
    data.append([[], []])


with open(filename, "r") as f:
    for line in f:
        steps, distance, weight = line.split()
        steps = int(steps)
        distance = float(distance)
        weight = float(weight)
        data[steps][0].append(distance)
        data[steps][1].append(weight)

Weights = []
for i in range(len(data)):
    data[i] = [np.array(data[i][0]), np.array(data[i][1])]
    Weights.append(sum(data[i][1]))
    data[i][1] /= Weights[-1]

def f(x, A, B):
    return A * x**B

Weights = np.array(Weights)
x = np.linspace(0, maxLength, maxLength + 1)
R = np.array([sum(d[0] * d[1]) for d in data])
sigmas = []

for i in range(maxLength + 1):
    sigma = (sum((data[i][0] - R[i])**2 * data[i][1]**2))**.5
    sigmas.append(sigma)

sigmas = np.array(sigmas)

results = curve_fit(f, x[lFB:], R[lFB:], (1, 0.75), sigma = sigmas[lFB:])
print(results)

plt.plot(x, R)
plt.errorbar(x, R, sigmas)
plt.plot(x, f(x, *results[0]), "--")

plt.show()
