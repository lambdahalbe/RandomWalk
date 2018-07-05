import matplotlib.pylab as plt
import numpy as np
from scipy.optimize import curve_fit

#filename = "triangular_meta.txt"
filename = "hexagonal_meta.txt"
lfb = 200  # lower fit boundary

line_beginnings = ["Datapoints per Length: ",
                   "Grand Canonical Partition Sum: ",
                   "EndToEndDistances: ",
                   "Std: "]
corresponding_variables = ["dppl", "Z", "R", "sR"]


with open(filename, "r") as f:
    for line in f:
        for i in range(len(line_beginnings)):
            if line.startswith(line_beginnings[i]):
                start_index = line.index("[")
                exec(corresponding_variables[i] + "=np.array(" + line[start_index:] + ")")

N = np.array(range(len(R)))

def f(x, A, B):
    return A * x**B

def chi2(x, y, sy, f):
    return sum((y - f(x))**2 / sy**2)/len(y) 

results = curve_fit(f, N[lfb:], R[lfb:], sigma=sR[lfb:])
print(results)
chi = chi2(N[lfb:], R[lfb:], sR[lfb:], lambda x: f(x, *results[0]))
print(chi)
plt.errorbar(N, R, sR)
plt.plot(N, f(N, *results[0]), "r--")
plt.semilogx()
plt.semilogy()
plt.grid()
plt.show()

plt.plot(N, dppl)
#plt.ylim([1, 2 * max(dppl)])
#plt.semilogy()
plt.show()
