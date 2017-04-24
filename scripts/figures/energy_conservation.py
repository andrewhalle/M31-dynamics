import rebound
import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt
import os
import sys

sim_number = sys.argv[1].zfill(3)
initial = rebound.Simulation.from_file("../../logs/suite/" + sim_number + "/000000000.log")
initial_energy = initial.calculate_energy()

sims = os.listdir("../../logs/suite/" + sim_number)
sims.sort()
sims.pop()
i = 1
data = []

while i < len(sims):
    sim = rebound.Simulation.from_file("../../logs/suite/" + sim_number + "/" + sims[i])
    data.append([i, (sim.calculate_energy() - initial_energy) / initial_energy])
    i += 1

x = [a[0] for a in data]
y = [a[1] for a in data]

plt.plot(x, y, 'k')
plt.savefig("../../images/conservation/energy.png")
