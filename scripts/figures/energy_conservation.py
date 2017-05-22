import rebound
import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt
import os
import sys

sys.path.append("../include")
from universal_logs import *

sim_number = sys.argv[1].zfill(3)
initial = restore("../../logs/suite_u/" + sim_number + "/000000000.logu")
initial_energy = initial.calculate_energy()

sims = os.listdir("../../logs/suite_u/" + sim_number)
sims.sort()
sims.pop()
i = 1
data = []

while i < len(sims):
    sim = restore("../../logs/suite_u/" + sim_number + "/" + sims[i])
    data.append([i, (sim.calculate_energy() - initial_energy) / initial_energy])
    i += 1

x = [a[0] for a in data]
y = [a[1] for a in data]

plt.plot(x, y, 'k')
plt.savefig("../../images/conservation/energy/" + sim_number + ".png")
