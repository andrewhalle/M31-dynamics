import rebound
import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

def get_r_vector(sim, particle):
    com = sim.calculate_com()
    return np.array([particle.x - com.x, particle.y - com.y, particle.z - com.z])

def get_v_vector(sim, particle):
    com = sim.calculate_com()
    return np.array([particle.vx - com.vx, particle.vy - com.vy, particle.vz - com.vz])

def get_h_vector(sim, particle):
    r = get_r_vector(sim, particle)
    v = get_v_vector(sim, particle)
    return np.cross(r, v)

def get_e_vector(sim, particle):
    r = get_r_vector(sim, particle)
    v = get_v_vector(sim, particle)
    h = get_h_vector(sim, particle)
    return (np.cross(v, h) / (sim.G * sim.particles[0].m)) - (r / np.linalg.norm(r))

i = 0
while i < 15000000:
    sim = rebound.Simulation.from_file("../logs/long/" + str(i).zfill(9) + ".log")
    ps = [p for p in sim.particles if p.id != 0]
    data =[]
    for p in ps:
        o = p.calculate_orbit()
        e = get_e_vector(sim, p)
        data.append([e[0], e[1], o.e])
    ex = [a[0] for a in data]
    ey = [a[1] for a in data]
    e = [a[2] for a in data]
    plt.scatter(ex, ey, c=e, cmap="jet", vmin=0, vmax=1)
    plt.colorbar(label="Eccentricity")
    plt.xlabel("x component")
    plt.ylabel("y component")
    plt.xlim([-1, 1])
    plt.ylim([-1, 1])
    plt.savefig("../images/e_vector/" + str(i).zfill(9) + ".png")
    plt.close("all")
    i += 10000
