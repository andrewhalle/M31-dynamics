import rebound
import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

def get_r(sim, particle):
    com = sim.calculate_com()
    return np.array([particle.x - com.x, particle.y - com.y, particle.z - com.z])

def get_v(sim, particle):
    com = sim.calculate_com()
    return np.array([particle.vx - com.vx, particle.vy - com.vy, particle.vz - com.vz])

def get_h(sim, particle):
    r = get_r(sim, particle)
    v = get_v(sim, particle)
    return np.cross(r, v)

def get_e(sim, particle):
    r = get_r(sim, particle)
    v = get_v(sim, particle)
    h = get_h(sim, particle)
    first_term = (np.cross(v, h)) / (sim.G * sim.particles[0].m)
    second_term = (r) / (np.linalg.norm(r))
    return first_term - second_term

def get_ie(sim, particle):
    e = get_e(sim, particle)
    ehat = (e) / (np.linalg.norm(e))
    ex = ehat[0]
    ey = ehat[1]
    return np.arctan2(ey, ex)

def calc_difference(angle1, angle2):
    diff = angle2 - angle1
    if diff > np.pi:
        return diff - (2 * np.pi)
    elif diff < -np.pi:
        return diff + (2 * np.pi)
    else:
        return diff

i = 0
while i < 14950000:
    sim1 = rebound.Simulation.from_file("../logs/long/" + str(i).zfill(9) + ".log")
    sim2 = rebound.Simulation.from_file("../logs/long/" + str(i + 50000).zfill(9) + ".log")
    ps1 = [p for p in sim1.particles if p.id != 0]
    ps2 = [p for p in sim2.particles if p.id != 0]
    data = []
    for p1, p2 in zip(ps1, ps2):
        o = p1.calculate_orbit()
        ie1 = get_ie(sim1, p1)
        ie2 = get_ie(sim2, p2)
        diff = calc_difference(ie1, ie2)
        data.append([o.a, diff, ie1])
    a = [x[0] for x in data]
    diff = [x[1] for x in data]
    ie = [x[2] for x in data]
    plt.scatter(a, diff, c=ie, cmap="jet", vmin=-np.pi, vmax=np.pi)
    plt.axhline(y=0, c='k', ls='dashed')
    plt.xlim([0, 600000])
    plt.ylim([-np.pi/4, np.pi/4])
    plt.colorbar(label="ie")
    plt.xlabel("Semi-major axis")
    plt.ylabel("Precession")
    plt.savefig("../images/disk_splitter_ie/" + str(i).zfill(9) + ".png")
    plt.close("all")
    i += 10000
