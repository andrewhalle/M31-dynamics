import rebound
import matplotlib as mpl
import matplotlib.cm as cm
import numpy as np
mpl.use("Agg")
import matplotlib.pyplot as plt

def get_f_vector(sim, particle):
    ps = [p for p in sim.particles if p.id != particle.id]
    fx = 0
    fy = 0
    fz = 0
    for p in ps:
        x_dist = p.x - particle.x
        y_dist = p.y - particle.y
        z_dist = p.z - particle.z
        dist = np.sqrt(x_dist**2 + y_dist**2 + z_dist**2)
        x_force = (sim.G * particle.m * p.m * x_dist) / (dist**3)
        y_force = (sim.G * particle.m * p.m * y_dist) / (dist**3)
        z_force = (sim.G * particle.m * p.m * z_dist) / (dist**3)
        fx += x_force
        fy += y_force
        fz += z_force
    return np.array([fx, fy, fz])

def get_fnonkep_vector(sim, particle):
    ps = [p for p in sim.particles if (p.id != particle.id and p.id != 0)]
    fx = 0
    fy = 0
    fz = 0
    for p in ps:
        x_dist = p.x - particle.x
        y_dist = p.y - particle.y
        z_dist = p.z - particle.z
        dist = np.sqrt(x_dist**2 + y_dist**2 + z_dist**2)
        x_force = (sim.G * particle.m * p.m * x_dist) / (dist**3)
        y_force = (sim.G * particle.m * p.m * y_dist) / (dist**3)
        z_force = (sim.G * particle.m * p.m * z_dist) / (dist**3)
        fx += x_force
        fy += y_force
        fz += z_force
    return np.array([fx, fy, fz])


def get_r_vector(sim, particle):
    com = sim.calculate_com()
    return np.array([particle.x - com.x, particle.y - com.y, particle.z - com.z])

def get_v_vector(sim, particle):
    com = sim.calculate_com()
    return np.array([particle.vx - com.vx, particle.vy - com.vy, particle.vz - com.vz])

def get_h_vector(sim, particle):
    r = get_r_vector(sim, particle)
    v = get_v_vector(sim, particle)
    return np.cross(r, v)

def get_e_vector(sim, particle):
    r = get_r_vector(sim, particle)
    v = get_v_vector(sim, particle)
    h = get_h_vector(sim, particle)
    return (np.cross(v, h) / (sim.G * sim.particles[0].m)) - (r / np.linalg.norm(r))

def get_edot_vector(sim, particle):
    f = get_f_vector(sim, particle)
    f_nonkep = get_fnonkep_vector(sim, particle)
    h = get_h_vector(sim, particle)
    v = get_v_vector(sim, particle)
    r = get_r_vector(sim, particle)
    tau = np.cross(r, f)
    return ((np.cross(f_nonkep / particle.m, h)) / (sim.G * sim.particles[0].m)) + ((np.cross(v, tau / particle.m)) / (sim.G * sim.particles[0].m))

def copy_sim(sim):
    new_sim = rebound.Simulation()
    new_sim.units = ('AU', 'yr', 'Msun')
    ps = sim.particles
    for p in ps:
        new_sim.add(m=p.m, x=p.x, y=p.y, z=p.z, vx=p.vx, vy=p.vy, vz=p.vz, id=p.id)
    return new_sim

def precess(sim, particle):
    sim = copy_sim(sim)
    particle = [p for p in sim.particles if p.id == particle.id][0]
    o = particle.calculate_orbit()
    mean_anom = o.M
    ident = particle.id
    sim.remove(particle.id)
    angles = np.linspace(0, 2 * np.pi, 100)
    edot = np.array([0, 0, 0])
    for angle in angles:
        sim.add(m=p.m, a=o.a, e=o.e, inc=o.inc, omega=o.omega, Omega=o.Omega, M=angle, id=ident)
        new_p = [p for p in sim.particles if p.id == ident][0]
        edot = edot + get_edot_vector(sim, new_p)
        sim.remove(new_p.id)
    sim.add(m=p.m, a=o.a, e=o.e, inc=o.inc, omega=o.omega, Omega=o.Omega, M=0, id=ident)
    new_p = [p for p in sim.particles if p.id == ident][0]
    vp = get_v_vector(sim, new_p)
    vp_unit = vp / np.linalg.norm(vp)
    return np.dot(edot, vp_unit)


i = 0
while i < 15000000:
    sim = rebound.Simulation.from_file("../logs/long/" + str(i).zfill(9) + ".log")
    ps = [p for p in sim.particles if p.id != 0]
    data = []
    for p in ps:
        o = p.calculate_orbit()
        data.append([o.a, precess(sim, p), o.e])
    a = [a[0] for a in data]
    pr = [a[1] for a in data]
    e = [a[2] for a in data]
    plt.scatter(a, pr, c=e, cmap='jet', vmin=0, vmax=1)
    plt.colorbar(label="Eccentricity")
    plt.xlabel("Semi-major axis (AU)")
    plt.xlim([0, 600000])
    plt.ylabel("Precession")
    plt.ylim([-0.01, 0.01])
    plt.savefig("../images/disk_splitter/" + str(i).zfill(9) + ".png")
    plt.close("all")
    i += 10000
