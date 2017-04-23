import numpy as np
import os

startNum = 0

i = startNum
while i < startNum + 2000:
    u = np.random.uniform(0, 1)
    v = np.random.uniform(0, 1)

    phi = 2 * np.pi * u
    theta = np.arccos(2*v - 1)

    os.system("python density_start.py " + str(theta) + " " + str(phi) + " " + str(i).zfill(5))
    i += 1
