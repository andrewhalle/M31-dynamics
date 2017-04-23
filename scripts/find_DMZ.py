import rebound
import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pickle

i = 0
data = []
while i < 15000000:
    sim = rebound.Simulation.from_file("../logs/long/" + str(i).zfill(9) + ".log")
    orbits = sim.calculate_orbits()
    a = [o.a for o in orbits]
    a = sorted(a)
    data.append([i, a[79]])
    i += 10000
pickle.dump(data, open("../images/find_DMZ/data.txt", "wb"))
t = [a[0] for a in data]
DMZ = [a[1] for a in data]
plt.plot(t, DMZ, 'k')
plt.savefig("../images/find_DMZ/DMZ.png")
