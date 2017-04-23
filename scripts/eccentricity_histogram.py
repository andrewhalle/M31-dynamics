import rebound
import numpy as np
import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt

i = 0
while i < 15000000:
    sim = rebound.Simulation.from_file("../logs/long/" + str(i).zfill(9) + ".log")
    orbits = sim.calculate_orbits()
    e = [o.e for o in orbits]
    n, bins, patches = plt.hist(e, 50, normed=1, facecolor='green')
    plt.xlabel("Eccentricity")
    plt.xlim([0, 1])
    plt.ylabel("Frequency")
    plt.ylim([0, 12])
    plt.savefig("../images/eccentricity_histogram/" + str(i).zfill(9) + ".png")
    plt.close("all")
    i += 10000
