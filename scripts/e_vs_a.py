import rebound
import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import os

sim = rebound.Simulation.from_file("../logs/suite/01/000005000.log")
ps = [p for p in sim.particles if p.id != 0]
data = []
start = 0
step = 0.5
while start < 4:
    bin = [p for p in ps if p.a > start and p.a < start + step]
    if len(bin) == 0:
        start += step
        continue
    e = [p.e for p in bin]
    data.append((start + (step / 2), np.average(e), np.std(e)))
    start += step

a = np.array([d[0] for d in data])
e = np.array([d[1] for d in data])
std = np.array([d[2] for d in data])
stdup = e + std
stdown = e - std
 

plt.plot(a, e, 'ko')
plt.plot(a, e, 'k')
plt.plot(a, stdup, 'bo')
plt.plot(a, stdup, 'b')
plt.plot(a, stdown, 'bo')
plt.plot(a, stdown, 'b')
plt.fill_between(a, e, stdup, facecolor='b', alpha=0.5)
plt.fill_between(a, stdown, e, facecolor='b', alpha=0.5)
plt.grid()
plt.xlabel("a")
plt.ylabel("e")
plt.ylim([0, 1])
plt.savefig("../e_vs_a.svg")
plt.close("all")
