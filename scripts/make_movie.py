import rebound
import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt
from andrew_OrbitPlot import OrbitPlot
import os

path = "../logs/suite/01/"
logs = os.listdir(path)
logs.sort()
logs.remove(logs[len(logs) - 1])
for log in logs:
    sim = rebound.Simulation.from_file(path + log)
    fig = OrbitPlot(sim, figsize=(10, 10), lim=4)
    plt.savefig("../images/movie02/" + log[:9] + ".png")
    plt.close("all")
