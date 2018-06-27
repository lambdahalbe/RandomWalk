# -*- coding: utf-8 -*-
"""
Created on Wed Jun 13 12:49:41 2018

@author: franz
"""

import matplotlib.pylab as plt
import numpy as np
from scipy.optimize import curve_fit


dataBySteps = {}
max_steps = -1

with open("triangulardat.txt", "r") as file:
    for line in file:
        steps, distance, weights = line.split()
        steps = int(steps)
        distance = float(distance)
        weights = float(weights)
        if steps > max_steps:
            max_steps = steps    
        if not (steps in dataBySteps):
            dataBySteps[steps] = []
        dataBySteps[steps].append((distance,weights))

# Summe der Gewichte pro Länge
SumWeightsPerLength = [sum([x[1] for x in listOfTuples]) for index,listOfTuples in dataBySteps.items()]

# Abstände pro Länge des Random Walks mit Gewichtung
NormalizedStepsPerLength = { index:[ elem[0]*elem[1]/SumWeightsPerLength[index] for elem in listOfTuples ] for index,listOfTuples in dataBySteps.items() }


# Summe der verschiedenen gewichteten Abstände einer Länge des Random Walkls
sumBySteps = [sum(elem) for index,elem in NormalizedStepsPerLength.items()] 


# Fehlerrechnung

# Berechnung von Nenner: (Mittelwert-Abstand)**2 * Gewichtung_Abstand 
denominator = { index:[ elem[1]* (sumBySteps[index] - elem[0])**2  for elem in listOfTuples ] for index,listOfTuples in dataBySteps.items() }

# Aufsummieren des Nenners und durch Summe der Gewichte dividieren für finalen Fehler
error_distance = np.array([np.sqrt(sum(elem)/SumWeightsPerLength[index]) for index,elem in denominator.items()])


x = np.array(sorted(dataBySteps.keys()))

def f(x, a, gamma):
    return a * x**gamma


# Plot hübsch machen
fig = plt.figure(figsize=(8,5))                                                            
ax = fig.add_subplot(1,1,1)
plt.grid()
ax.set_yscale('log')
ax.set_xscale('log')

results = curve_fit(f, x[100:], sumBySteps[100:], p0=[1, .5], sigma=error_distance[100:])
plt.plot(x, f(x, *results[0]), "--g", lw=2)
print(results)

chi2 = (sum((sumBySteps[5:] - f(x, *results[0])[5:])**2 / error_distance[5:]**2) / len(sumBySteps[5:]))
print("Chi")
print(chi2)

plt.plot(x, sumBySteps, "xr")
plt.errorbar(x, sumBySteps, yerr=error_distance, fmt="o", barsabove=True)
plt.plot(x, f(x, *results[0]), "--g", lw=2)
plt.show()
#plt.savefig("test.pdf")

