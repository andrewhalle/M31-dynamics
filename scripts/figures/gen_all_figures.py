import os

# conservation
sim_numbers = os.listdir("../../logs/suite_u/")
sim_numbers.sort()
for sim_number in sim_numbers:
    print(sim_number)
    os.system("python angularMomentum_conservation.py " + sim_number)   #angular momentum
    os.system("python energy_conservation.py " + sim_number)            #energy

#disk_imager
os.system("python disk_imager.py")
os.system("python disk_imager_velocity.py")
os.system("python disk_imager_dispersion.py")

#avg_e_vs_time_all
os.system("python avg_e_vs_time_all.py")

#disk_splitter
os.system("python disk_splitter_plots.py")

#e_vs_a_avg
os.system("python e_vs_a_avg.py")

#e_vs_time
os.system("python e_vs_time.py")

#inc_vs_a_avg
os.system("python inc_vs_a_avg.py")

#initial_e_vs_mass_ratio
os.system("python initial_e_vs_mass_ratio.py")
