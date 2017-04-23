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

path = "../logs/long/"
look_ahead = 5
logs = os.listdir(path)
logs.sort()
num_logs = len(logs)
i = 0

while i < 1500:
    sim1 = rebound.Simulation.from_file(path + logs[i])
    sim2 = rebound.Simulation.from_file(path + logs[i + look_ahead])
    ps1 = [p for p in sim1.particles if p.id != 0]
    ps2 = [p for p in sim2.particles if p.id != 0]
    x = 0
    data1 = []
    while x < len(ps1):
        ie1 = get_ie(sim1, ps1[x])
        ie2 = get_ie(sim2, ps2[x])
        delta = calc_difference(ie1, ie2)
        a = ps1[x].calculate_orbit().a
        if a > 0:
            data1.append([a, delta, ie1])
        x += 1
    
    data2 = []

    smallest = 0
    biggest = 600000
    step = (biggest - smallest) / 10
    counter = smallest
    while counter < biggest:
        bin = [a for a in data1 if (a[0] >= counter and a[0] < counter + step)]
        if len(bin) == 0:
            counter += step
            continue
        a = (2 * counter + step) / 2
        mean_delta = np.average([a[1] for a in bin])
        stdev = np.std([a[2] for a in bin])
        data2.append([a, mean_delta, stdev])
        counter += step

    a = [a[0] for a in data2]
    mean_delta = [a[1] for a in data2]
    stdev = [a[2] for a in data2]

    fig, ax1 = plt.subplots()
    ax1.plot(a, mean_delta, "bo")
    ax1.plot(a, mean_delta, "b", lw=2)
    plt.axhline(c='k', ls="dashed")
    ax1.set_xlabel("Semi-major axis")
    ax1.set_ylabel(r"$\Delta i_e$", color="b")
    ax1.set_ylim([-np.pi/6, np.pi/6])
    ax1.set_xlim([0, 600000])

    ax2 = ax1.twinx()
    ax2.plot(a, stdev, "ro")
    ax2.plot(a, stdev, "r", lw=2)
    ax2.set_ylabel(r"$\sigma_{i_e}$", color="r")
    ax2.set_ylim([0, np.pi/2])
    ax2.set_xlim([0, 600000])


    plt.savefig("../images/disk_splitter_ie_mean/" + logs[i][0:9] + ".png")
    plt.close("all")
    i += 1
    
    
