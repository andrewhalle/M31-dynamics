import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import rebound
import pickle
import os
import sys
sys.path.append("..")
from include.disk_splitter_include import disk_splitter

def get_completed_sims():
    sims = os.listdir("../logs/suite")
    sims.sort()
    sims.pop()
    return sims

def get_mass_fraction(sim, cutoff):
    p = [p.a for p in sim.particles[1:] if p.a > cutoff]
    return len(p)/len(sim.particles[1:])

def get_data_one_sim(sim_num):
    initial_e = rebound.Simulation.from_file("../logs/suite/" + sim_num + "/000000000.log").particles[1].e
    num_cols = len(pickle.load(open("../logs/suite/" + sim_num + "/collision_events.txt", "rb")))
    cutoff_point = disk_splitter("../logs/suite/" + sim_num)
    mass_fraction = get_mass_fraction(rebound.Simulation.from_file("../logs/suite/" + sim_num + "/000009980.log"), cutoff_point)
    return str(initial_e) + "     " + str(mass_fraction) + "     " + str(num_cols) + "\n"

sims = get_completed_sims()
data = open("../images/initial_e_vs_mass_ratio/data.txt", "w")
for sim in sims:
    data.write(get_data_one_sim(sim))
    
data.close()
