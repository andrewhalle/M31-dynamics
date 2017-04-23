import rebound
import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import os

stars = [10, 20, 30]

path = "../logs/suite/02/"
logs = os.listdir(path)
logs.sort()
del logs[len(logs) - 1]
data = []
for log in logs:
    sim = rebound.Simulation.from_file(path + log)
    ps = [p for p in sim.particles if p.id in stars]
    data.append([(sim.t, 1 - ps[0].e), (sim.t, 1 - ps[1].e), (sim.t, 1 - ps[2].e)])
    
t = [d[0][0]/20 for d in data]
e1 = [d[0][1] for d in data]
e2 = [d[1][1] for d in data]
e3 = [d[2][1] for d in data]

plt.semilogy(t, e1, 'k', lw=2)
plt.semilogy(t, e2, 'b', lw=2)
plt.semilogy(t, e3, 'r', lw=2)
plt.xlabel("Time (Periods of innermost orbit)")
plt.ylabel("1 - e")
plt.grid()

plt.savefig("../e_vs_time.svg")
plt.close("all")

