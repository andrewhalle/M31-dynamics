import pickle
import numpy as np

sim_number = 0

while sim_number < 9:
    collisions = pickle.load(open("../logs/suite/" + str(sim_number).zfill(3) + "/collision_events.txt", "rb"))
    times = [0]
    total = [0]
    rate = 0
    i = 1
    for col in collisions:
        times.append(col[1][0])
        total.append(i)
        i += 1

        if len(collisions) == 0:
            rate = 0
        else:
            rate = np.polyfit(times, total, 1)[0]
    data = open("../images/collision_rate/rates.txt", "a")
    data.write(str(sim_number) + " " + str(rate) + " " + str(len(collisions)) + "\n")
    data.close()
    sim_number += 1
