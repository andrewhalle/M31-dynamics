import rebound
import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

def get_r(sim, particle):
    com = sim.calculate_com()
    return np.array([p.x - com.x, p.y - com.y, p.z - com.z])

def get_v(sim, particle):
    com = sim.calculate_com()
    return np.array([p.vx - com.vx, p.vy - com.vy, p.vz - com.vz])



def get_f(sim, particle):
    
