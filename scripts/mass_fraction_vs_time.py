import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import rebound
from disk_splitter_copy import disk_splitter
import os

def get_mass_fraction(sim, limit):
    outer = [p for p in sim.particles[1:] if p.a > limit]
    return len(outer)/len(sim.particles[1:])

sim_number = "012"
divide = disk_splitter("../logs/suite/" + sim_number)
sims = os.listdir("../logs/suite/" + sim_number)
sims.sort()
data = []
for sim in sims[:len(sims) - 1]:
    s = rebound.Simulation.from_file("../logs/suite/" + sim_number + "/" + sim)
    data.append([s.t, get_mass_fraction(s, divide)])

t = [a[0] for a in data]
mf = [a[1] for a in data]

plt.plot(t, mf, 'b')
plt.savefig("../images/mass_fraction_vs_time/mfvt.pdf")
