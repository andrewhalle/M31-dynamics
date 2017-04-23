import rebound
import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt

initial = rebound.Simulation.from_file("run/high_mass_1/000000000.log")
initial_energy = initial.calculate_energy()

i = 0
data = []

while i < 15000000:
    sim = rebound.Simulation.from_file("run/high_mass_1/" + str(i).zfill(9) + ".log")
    data.append([i, (sim.calculate_energy() - initial_energy) / initial_energy])
    i += 10000

x = [a[0] for a in data]
y = [a[1] for a in data]

plt.plot(x, y, 'k')
plt.savefig("test.png")
