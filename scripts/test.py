import rebound
import os
import numpy as np

path = "../logs/suite/"
sims = os.listdir(path)
sims.sort()


e_s = []
for sim in sims:
    t_s = os.listdir(path + sim)
    t_s.sort()
    t_s.pop()
    s = rebound.Simulation.from_file(path + sim + "/" + t_s[0])
    e = [p.e for p in s.particles[1:]]
    e_s.append(np.average(e))

print(e_s)
