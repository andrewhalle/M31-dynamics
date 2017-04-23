import rebound
import numpy as np
import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt

def calculate_angular_momentum(sim):
    com = sim.calculate_com()
    j = np.array([0, 0, 0])
    for p in sim.particles:
        r = np.array([p.x - com.x, p.y - com.y, p.z - com.z])
        v = np.array([p.vx - com.vx, p.vy - com.vy, p.vz - com.vz])
        j = j + np.cross(r, v)
    return np.linalg.norm(j)
        

initial = rebound.Simulation.from_file("../logs/high_mass_1/000000000.log")
initial_mom = calculate_angular_momentum(initial)

data = []
i = 0
while i < 15000000:
    sim = rebound.Simulation.from_file("../logs/high_mass_1/" + str(i).zfill(9) + ".log")
    data.append([i, (calculate_angular_momentum(sim) - initial_mom) / initial_mom])
    i += 10000

x = [a[0] for a in data]
y = [a[1] for a in data]

plt.plot(x, y, 'k')
plt.xlabel("Time")
plt.ylabel("Error")
plt.savefig("../images/conservation/angular.png")
