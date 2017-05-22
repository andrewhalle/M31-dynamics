import rebound
import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import os
import pickle
from universal_logs import *

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

def ie_stdev(ies):
    mean = np.average(ies)
    devs = [calc_difference(mean, ie) for ie in ies]
    square_devs = [dev**2 for dev in devs]
    var = np.average(square_devs)
    return np.sqrt(var)

def disk_splitter(path):
    look_ahead = 5
    logs = os.listdir(path)
    logs.sort()
    i = 0
    data = [["", "", ""], ["", "", ""], ["", "", ""], ["", "", ""], ["", "", ""], ["", "", ""], ["", "", ""], ["", "", ""], ["", "", ""], ["", "", ""]]

    while i < len(logs) - look_ahead:
        sim1 = restore(path + "/" + logs[i])
        sim2 = restore(path + "/" + logs[i + look_ahead])
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
            
        smallest = 0
        biggest = 4
        step = (biggest - smallest) / 10
        counter = smallest
        bin_index = 0
        while counter < biggest - 0.1:
            bin = [a for a in data1 if (a[0] >= counter and a[0] < counter + step)]
            bin_list = data[bin_index]
            if len(bin) == 0:
                counter += step
                bin_index += 1
                continue
            a = counter + (step / 2)
            mean_delta = np.average([a[1] for a in bin])
            stdev = ie_stdev([a[2] for a in bin])
            if bin_list[0] == "":
                bin_list[0] = [a]
                bin_list[1] = [mean_delta]
                bin_list[2] = [stdev]
            else:
                bin_list[1].append(mean_delta)
                bin_list[2].append(stdev)
            counter += step
            bin_index += 1
        i += 1

    data = [d for d in data if d[0] != ""]
    a = [d[0] for d in data]
    mean_delta = [np.average(d[1]) for d in data]
    i = len(mean_delta) - 1
    while i >= 0 and mean_delta[i] < 0:
        i -= 1
    if i == -1:
        return a[0][0]
    return a[i][0]
        
