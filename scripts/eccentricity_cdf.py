import rebound
import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

i = 0
while i < 15000000:
    sim = rebound.Simulation.from_file("../logs/long/" + str(i).zfill(9) + ".log")
    orbits = sim.calculate_orbits()
    e = [o.e for o in orbits]
    e.sort()
    e = np.array(e)
    cumnum = np.arange(1, len(e) + 1, 1)
    cumfreq = cumnum / len(e)
    e = np.insert(e, 0, 0)
    e = np.append(e, 1)
    cumfreq = np.insert(cumfreq, 0, 0)
    cumfreq = np.append(cumfreq, 1)
    plt.plot(e, cumfreq, 'b')
    plt.xlim([0, 1])
    plt.ylim([0, 1])
    plt.xlabel("Eccentricity")
    plt.ylabel("Frequency")
    plt.savefig("../images/eccentricity_cdf/" + str(i).zfill(9) + ".png")
    plt.close("all")
    i += 10000
