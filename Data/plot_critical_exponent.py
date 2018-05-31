import matplotlib.pylab as plt
import numpy as np
from collections import defaultdict
from scipy.optimize import curve_fit

data = defaultdict(list)
max_steps = -1

with open("critical_exponent_data.txt", "r") as file:
    for line in file:
        steps, distance = line.split()
        if int(steps) > max_steps:
            max_steps = int(steps)
        data[int(steps)].append(float(distance))

x = np.linspace(0, max_steps, max_steps + 1)
y = np.array([np.mean(data[i]) for i in x])
s_y = np.array([np.std(data[i]) / len(data[i])**.5 for i in x])

def f(x, a, gamma):
    return a * x**gamma

results = curve_fit(f, x[5:], y[5:], p0=[1, .5], sigma=s_y[5:])
print(results)

chi2 = (sum((y[5:] - f(x, *results[0])[5:])**2 / s_y[5:]**2) / len(y[5:]))
print(chi2)
plt.plot(x, y, "xr")
plt.errorbar(x, y, yerr=s_y, color="red")
plt.plot(x, f(x, *results[0]), "--b")
plt.show()
