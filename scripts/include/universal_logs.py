import rebound
import os

def convert(path_to_sim, output_file_name):
    sim = rebound.Simulation.from_file(path_to_sim)
    out = open(output_file_name, "w")
    for p in sim.particles:
        out.write(str(p.id) + ", " + str(p.m) + ", " + str(p.x) + ", " + str(p.y) + ", " + str(p.z) + ", " + str(p.vx) + ", " + str(p.vy) + ", " + str(p.vz) + "\n")
    out.write(str(sim.t))
    out.close()

def restore(path_to_sim):
    sim = rebound.Simulation()
    file = open(path_to_sim)
    lines = file.readlines()
    for i in range(len(lines) - 1):
        row = lines[i].split(", ")
        sim.add(id=int(row[0]), m=float(row[1]), x=float(row[2]), y=float(row[3]), z=float(row[4]), vx=float(row[5]), vy=float(row[6]), vz=float(row[7]))
    sim.t = float(lines[-1])
    file.close()
    return sim

if __name__ == "__main__":
    os.system("mkdir ../../logs/suite_u")
    sim_numbers = os.listdir("../../logs/suite")
    sim_numbers.sort()
    for sim_number in sim_numbers:
        os.system("mkdir ../../logs/suite_u/" + sim_number)
        sims = os.listdir("../../logs/suite/" + sim_number)
        sims.sort()
        sims.pop()
        for sim in sims:
            convert("../../logs/suite/" + sim_number + "/" + sim, "../../logs/suite_u/" + sim_number + "/" + sim + "u")

