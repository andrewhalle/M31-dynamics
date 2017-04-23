import rebound
import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import os

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

def atan(y, x):
    if x == 0:
        if y > 0:
            return np.pi / 2
        elif y < 0:
            return -np.pi / 2
        else:
            return np.nan
    else:
        theta = np.arctan(y / x)
        if x < 0:
            if y > 0:
                theta = theta + np.pi
            elif y < 0:
                theta = theta - np.pi
        return theta

def get_ie(sim, particle):
    e = get_e(sim, particle)
    ehat = (e) / (np.linalg.norm(e))
    ex = ehat[0]
    ey = ehat[1]
    return atan(ey, ex)

logs = os.listdir("../logs/suite/00")
for log in logs:
    sim = rebound.Simulation.from_file("../logs/suite/00/" + log)
    ps = [p for p in sim.particles if p.id != 0]
    ie = [get_ie(sim, p) for p in ps]
    ie.sort()
    ie = np.array(ie)
    cumnum = np.arange(1, len(ie) + 1, 1)
    cumfreq = cumnum / len(ie)
    ie = np.insert(ie, 0, -np.pi)
    ie = np.append(ie, np.pi)
    cumfreq = np.insert(cumfreq, 0, 0)
    cumfreq = np.append(cumfreq, 1)
    plt.plot(ie, cumfreq, 'b')
    plt.xlim([-np.pi, np.pi])
    plt.ylim([0, 1])
    plt.xlabel(r'i_e')
    plt.ylabel("Frequency")
    plt.savefig("../images/test/" + log[0:9] + ".png")
    plt.close("all")
