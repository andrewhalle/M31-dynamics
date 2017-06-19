# Same as disk imager, but generates     #
# dispersion of "spectrum" instead of    #
# observed image. Accomplishes this by   #
# simply imaging standard deviation of   #
# velocities along line of sight instead #
# of sum of velocities.                  #

import rebound
import numpy as np
import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.colors import Normalize
import scipy.misc
import sys

sys.path.append("../include")
from universal_logs import *
from M31config import Config

c = Config("disk_imager_dispersion.config")
x_angle = c.x_angle * (np.pi / 180)
y_angle = c.y_angle * (np.pi / 180)
z_angle = c.z_angle * (np.pi / 180)

rot_x = np.array([[1, 0, 0], [0, np.cos(x_angle), -np.sin(x_angle)], [0, np.sin(x_angle), np.cos(x_angle)]])
rot_y = np.array([[np.cos(y_angle), 0, np.sin(y_angle)], [0, 1, 0], [-np.sin(y_angle), 0, np.cos(y_angle)]])
rot_z = np.array([[np.cos(z_angle), -np.sin(z_angle), 0], [np.sin(z_angle), np.cos(z_angle), 0], [0, 0, 1]])

def orbit_density(sim, particle):
    period = np.sqrt(((4 * np.pi**2) / (sim.G * sim.particles[0].m)) * particle.a**3)
    positions = []
    velocities = []
    t = np.linspace(0, 2*np.pi, 500)
    for i in range(499):
        sim.add(m=particle.m, a=particle.a, e=particle.e, inc=particle.inc, omega=particle.omega, Omega=particle.Omega, f=t[i], id=10000)
        sim.add(m=particle.m, a=particle.a, e=particle.e, inc=particle.inc, omega=particle.omega, Omega=particle.Omega, f=t[i + 1], id=10001)
        p1, p2 = [p for p in sim.particles if (p.id == 10000 or p.id == 10001)]

        #rotate
        r1 = np.array([p1.x, p1.y, p1.z]).reshape((3, 1))
        r2 = np.array([p2.x, p2.y, p2.z]).reshape((3, 1))
        r1 = np.dot(rot_x, np.dot(rot_y, np.dot(rot_z, r1)))
        r2 = np.dot(rot_x, np.dot(rot_y, np.dot(rot_z, r2)))

        v1 = np.array([p1.vx, p1.vy, p1.vz]).reshape((3, 1))
        v2 = np.array([p2.vx, p2.vy, p2.vz]).reshape((3, 1))
        v1 = np.dot(rot_x, np.dot(rot_y, np.dot(rot_z, r1)))
        v2 = np.dot(rot_x, np.dot(rot_y, np.dot(rot_z, r2)))

        positions.append(((r1[0][0], r1[1][0], r1[2][0]), (r2[0][0], r2[1][0], r2[2][0])))
        velocities.append((v1[2] + v2[2]) / 2)

        sim.remove(id=p1.id)
        sim.remove(id=p2.id)
    return (positions, velocities)

def plot_density(density):
    fig, ax = plt.subplots()
    positions, densities = density
    minimum = 0
    maximum = max(densities)
    norm = Normalize(vmin=minimum, vmax=maximum, clip=True)
    for i in range(len(positions)):
        p1, p2 = positions[i]
        d = densities[i]
        if d < 0:
            d = maximum
        ax.plot([p1[0], p2[0]], [p1[1], p2[1]], c=cm.Greys(norm(d)))
    ax.set_xlim([-2, 2])
    ax.set_ylim([-2, 2])
    ax.axis("equal")
    return fig
    
def get_all_densities(sim):
    particles = [p for p in sim.particles if p.id != 0]
    d = []
    i = 0
    for p in particles:
        print(i)
        i += 1
        d.append(orbit_density(sim, p))
    return d



#image generation
sim = restore("../../logs/suite_u/" + c.sim_number + "/" + c.sim)
limit = c.limit
image_width = 80
pixel_width = (2 * limit) / image_width
y = limit
d = get_all_densities(sim)
img = np.zeros((image_width, image_width))
for i in range(image_width):
    x = -limit
    print(y)
    for j in range(image_width):
        x_min = x
        x_max = x + pixel_width
        y_max = y
        y_min = y - pixel_width
        velocity_here = []
        for p in d:
            pos = p[0]
            vel = p[1]
            for k in range(len(pos)):
                x1 = pos[k][0][0]
                x2 = pos[k][1][0]
                y1 = pos[k][0][1]
                y2 = pos[k][1][1]
                if ((x1 > x_min and x1 < x_max) or (x2 > x_min and x2 < x_max)) and ((y1 > y_min and y1 < y_max) or (y2 > y_min and y2 < y_max)):
                    velocity_here.append(vel[k])
        if velocity_here == []:
            stdev = 0
        else:
            stdev = np.std(velocity_here)
        img[i, j] = stdev
        x += pixel_width
    y -= pixel_width
plt.imshow(img, cmap="jet")
plt.colorbar()
plt.scatter(40, 40, s=120, c="black", marker="*")
plt.savefig("../../images/disk_imager_dispersion/disk.png")
