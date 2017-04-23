import rebound
import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import os
from disk_splitter_copy import disk_splitter
from scipy.signal import savgol_filter

sim_number = "012"
divide = disk_splitter("../logs/suite/" + sim_number)
sims = os.listdir("../logs/suite/" + sim_number)
sims.sort()
data = []
sim = rebound.Simulation.from_file("../logs/suite/" + sim_number + "/" + sims[100])
inner = [p for p in sim.particles[1:] if p.a <= divide]
outer = [p for p in sim.particles[1:] if p.a > divide]
inner.sort(key=lambda x: x.a)
outer.sort(key=lambda x: x.a)
inner = inner[len(inner)//2:len(inner)//2 + 4]
outer = outer[len(outer)//2:len(outer)//2 + 4]
inner_ids = [p.id for p in inner]
outer_ids = [p.id for p in outer]
for s in sims[:len(sims) - 1]:
        sim = rebound.Simulation.from_file("../logs/suite/" + sim_number + "/" + s)
        inner = [p for p in sim.particles[1:] if p.id in inner_ids]
        outer = [p for p in sim.particles[1:] if p.id in outer_ids]
        if len(inner) > 0:
                j_inner = np.average([1 - p.e**2 for p in inner])
                q_inner = [np.percentile([1-p.e**2 for p in inner], 25), np.percentile([1-p.e**2 for p in inner], 75)]
        else:
                j_inner = 0
                q_inner = [0, 0]
        if len(outer) > 0:
                j_outer = np.average([1 - p.e**2 for p in outer])
                q_outer = [np.percentile([1-p.e**2 for p in outer], 25), np.percentile([1-p.e**2 for p in outer], 75)]
        else:
                j_outer = 0
                q_outer = [0, 0]
        time = sim.t
        data.append([time, j_inner, q_inner, j_outer, q_outer])

t = np.array([a[0] for a in data])
j_inner = np.array([a[1] for a in data])
q_inner = np.array([a[2] for a in data])
j_outer = np.array([a[3] for a in data])
q_outer = np.array([a[4] for a in data])

#j_inner = savgol_filter(j_inner, 31, 2)
#j_outer = savgol_filter(j_outer, 31, 2)

plt.plot(t, j_inner, 'b')
plt.fill_between(t, [a[0] for a in q_inner], [a[1] for a in q_inner], facecolor="blue", alpha=0.5)
plt.plot(t, j_outer, 'orange')
plt.fill_between(t, [a[0] for a in q_outer], [a[1] for a in q_outer], facecolor="orange", alpha=0.5)
plt.xlabel("Time")
plt.ylabel(r"$\langle 1 - e^2 \rangle$", rotation=0, fontsize=14, labelpad=15)
plt.tight_layout()
plt.savefig("../images/ugly_plot/ugly_plot.pdf")
