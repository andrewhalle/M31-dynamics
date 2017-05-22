import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import rebound
import pickle
import os
import sys

sys.path.append("../include")
from disk_splitter_include import disk_splitter
from universal_logs import *

def get_completed_sims():
    sims = os.listdir("../../logs/suite_u")
    sims.sort()
    return sims

def get_mass_fraction(sim, cutoff):
    p = [p.a for p in sim.particles[1:] if p.a > cutoff]
    return len(p)/len(sim.particles[1:])

def get_data_one_sim(sim_num):
    initial_e = restore("../../logs/suite_u/" + sim_num + "/000000000.logu").particles[1].e
    cutoff_point = disk_splitter("../../logs/suite_u/" + sim_num)
    mass_fraction = get_mass_fraction(restore("../../logs/suite_u/" + sim_num + "/000009980.logu"), cutoff_point)
    return str(initial_e) + "     " + str(mass_fraction) + "\n"

sims = get_completed_sims()
data = open("../../images/initial_e_vs_mass_ratio/data.txt", "w")
for sim in sims:
    print(sim)
    data.write(get_data_one_sim(sim))
data.close()
