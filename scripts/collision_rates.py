import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt

rates = open("../images/collision_rate/rates.txt", "r")
e = []
r = []
num = []

for line in rates:
    parsed = line.split()
    e.append(parsed[0])
    r.append(parsed[1])
    num.append(parsed[2])

plt.plot(e, r, "bo")
plt.xlabel("Initial eccentricity")
plt.ylabel("Collision rate")
plt.savefig("../images/collision_rate/rate.png")
plt.close("all")

plt.plot(e, num, "ro")
plt.xlabel("Initial eccentricity")
plt.ylabel("Total number of collisions")
plt.savefig("../images/collision_rate/number.png")
plt.close("all")
