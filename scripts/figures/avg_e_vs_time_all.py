# Generates graph of average eccentricity  #
# of the simulation versus time. Combines  #
# these graphs for all simulations.        #

import rebound
import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import os
import sys

sys.path.append("../include")
from universal_logs import *

jet = cm.get_cmap("jet")


path = "../../logs/suite_u/"
sims = os.listdir(path)
sims.sort()
global_data = []
for sim in sims:
    print(sim)
    t_s = os.listdir(path + sim)
    t_s.sort()
    data = []
    for t in t_s:
        sim_t = restore(path + sim + "/" + t)
        ps = sim_t.particles[1:]
        e_s = [p.e for p in ps]
        data.append([sim_t.t, np.average(e_s)])
    time = [a[0] for a in data]
    e = [a[1] for a in data]
    initial_e = e[0]
    global_data.append([initial_e, time, e])


for d in global_data:
    plt.plot(d[1], d[2], c=jet(d[0]))

plt.ylim([0, 1.5])
plt.savefig("../../images/avg_e_vs_time_all/plot.png")
plt.close("all")
