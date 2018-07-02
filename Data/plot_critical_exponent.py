import matplotlib.pylab as plt
import numpy as np
from collections import defaultdict
from scipy.optimize import curve_fit
from matplotlib.lines import Line2D

data = defaultdict(list)
max_steps = -1

with open("critital_exponent_hexagonal_notselfavoiding_1000.txt", "r") as file:
    for line in file:
        steps, distance = line.split()
        if int(steps) > max_steps:
            max_steps = int(steps)
        data[int(steps)].append(float(distance))

#x = np.linspace(0, max_steps, max_steps + 1)
x = np.array(sorted(data.keys()))
y = np.array([np.mean(data[i]) for i in x])
s_y = np.array([np.std(data[i], ddof=1) / len(data[i])**.5 for i in x])

def f(x, a, gamma):
    return a * x**gamma

results, error = curve_fit(f, x[150:], y[150:], p0=[1, .5], sigma=s_y[150:])

err = np.sqrt(np.diag(error))

chi2 = (sum((y[150:] - f(x, *results)[150:])**2 / s_y[150:]**2) / len(y[150:]))




# Plot hübsch machen
fig = plt.figure(figsize=(8,5))                                                            
ax = fig.add_subplot(1,1,1)
ax.set_yscale('log')
ax.set_xscale('log')

#Achsen verschönern
ticklabels = ax.get_xticklabels() + ax.get_yticklabels()
for label in ticklabels:
    label.set_fontsize(15)
ax.grid(which='both')
ax.grid(which='minor', alpha=0.2)                                                
ax.grid(which='major', alpha=0.8)                                      
plt.xlabel("Steps", fontsize = 15)
plt.ylabel(r"Average Distance", fontsize = 15)

def ezlegend(*dat, **args):
    dat = list(dat)
    for i, line in enumerate(dat):
        if not str(type(line)).startswith("<class 'matplotlib"):
            dat[i] = Line2D([],[], ls = "", label = line)
    plt.legend(**args, handles = dat, fontsize = 15)


#Sachen plotten
line1, = plt.plot(x, y, "xr", label = "Data")
plt.errorbar(x, y, yerr=s_y, fmt="o", barsabove=True)
line2, = plt.plot(x, f(x, *results), "--g", lw=2, label = r"Fit: d$_n$ = a $\cdot$ n$^\nu$")
ezlegend(line1, line2, "a = {}$\pm${}".format(round(results[0],2),round(err[0],2)), r"$\nu$ = {}$\pm${}".format(round(results[1],3),round(err[1],3)))

#plt.savefig("test.pdf")
plt.show()
