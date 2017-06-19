# Generates figure which shows change # 
# in total angular momentum of the    #
# simulation versus time              #

import rebound
import numpy as np
import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt
import sys
import os

sys.path.append("../include")
from universal_logs import *

def calculate_angular_momentum(sim):
    com = sim.calculate_com()
    j = np.array([0, 0, 0])
    for p in sim.particles:
        r = np.array([p.x - com.x, p.y - com.y, p.z - com.z])
        v = np.array([p.vx - com.vx, p.vy - com.vy, p.vz - com.vz])
        j = j + np.cross(r, v)
    return np.linalg.norm(j)
        
sim_number = sys.argv[1].zfill(3)
initial = restore("../../logs/suite_u/" + sim_number + "/000000000.logu")
initial_mom = calculate_angular_momentum(initial)

sims = os.listdir("../../logs/suite_u/" + sim_number)
sims.sort()
sims.pop()
data = []
i = 1
while i < len(sims):
    sim = restore("../../logs/suite_u/" + sim_number + "/" + sims[i])
    data.append([i, (calculate_angular_momentum(sim) - initial_mom) / initial_mom])
    i += 1

x = [a[0] for a in data]
y = [a[1] for a in data]

plt.plot(x, y, 'k')
plt.xlabel("Time")
plt.ylabel("Error")
plt.savefig("../../images/conservation/angular_momentum/" + sim_number + ".png")
