# run from m31_summer

import os
import rebound
import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

sim_number = "035"  #change this

sims = os.listdir("logs/suite/" + sim_number)
sims.sort()
sims.pop()

a = np.linspace(0, 5, 10)
inc = []

for sim in sims:
    s = rebound.Simulation.from_file("logs/suite/" + sim_number + "/" + sim)
    ps = [p for p in s.particles if p.id != 0]
    i = np.zeros(10)
    a_start = a[0]
    a_end = a[1]
    j = 1
    while j < 10:
        p = [x for x in ps if x.a >= a_start and x.a < a_end]
        incs = [x.inc for x in p]
        if len(incs) > 0:
            i[j - 1] = np.average(incs)
        else:
            i[j - 1] = 0
        a_start = a_end
        j += 1
        if j < 10:
            a_end = a[j]
    inc.append(i)

inc_avg = []
for i in range(10):
    inc_avg.append(np.average([x[i] for x in inc]))
plt.plot(a[:9], inc_avg[:9], 'b')
plt.plot(a[:9], inc_avg[:9], 'bo')
plt.xlabel("Semi-major axis")
plt.ylabel("Inclination")
plt.savefig("images/inc_vs_a_avg/" + sim_number + "_inc_vs_a_avg.png")
plt.close()
