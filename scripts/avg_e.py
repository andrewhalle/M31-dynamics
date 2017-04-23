import rebound
import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import os

jet = cm.get_cmap("jet")


path = "../logs/suite/"
sims = os.listdir(path)
sims.sort()
sims.pop()
global_data = []
for sim in sims:
    t_s = os.listdir(path + sim)
    t_s.sort()
    t_s.pop()
    data = []
    for t in t_s:
        sim_t = rebound.Simulation.from_file(path + sim + "/" + t)
        ps = sim_t.particles[1:]
        e_s = [p.e for p in ps]
        data.append([sim_t.t, np.average(e_s)])
    time = [a[0] for a in data]
    e = [a[1] for a in data]
    initial_e = e[0]
    global_data.append([initial_e, time, e])


for d in global_data:
    plt.plot(d[1], d[2], c=jet(d[0]))

plt.savefig("../images/avg_e/avg_e.pdf")
plt.close("all")
