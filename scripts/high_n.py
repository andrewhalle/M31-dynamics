import rebound
import numpy as np
import matplotlib as mpl
mpl.use('Agg') #only use this when computing on EC2
import matplotlib.pyplot as plt
import pickle

#######################
#            convenience functions      #
#######################

def get_a():
    x = np.random.uniform(1, 3.5)
    y = np.random.uniform(0, 1)
    fx = x**(-1)
    if y < fx:
        x = (x - 2.0) * 41253 + 309397
        return x
    else:
        return get_a()

def get_e():
    e = np.random.normal(loc=0.7, scale=0.1)
    if e > 0 and e < 1:
        return e
    return get_e()

def get_e_vector_proj(sim, central_body, particle):
    r_vec = np.array([particle.x, particle.y])
    v_vec = np.array([particle.vx, particle.vy])
    mu = sim.G * central_body.m
    e_vec = (((np.linalg.norm(v_vec)**2)/(mu)) - ((1)/(np.linalg.norm(r_vec))) * r_vec) - (((np.dot(r_vec, v_vec))/(mu))*v_vec)
    return e_vec
    
def get_direction_distribution(sim):
    ps = sim.particles
    black_hole = ps[0]
    i = 1
    directions = []
    while i < len(sim.particles):
        p = ps[i]
        e_vec = get_e_vector_proj(sim, black_hole, p)
        if e_vec[0] == 0:
            if e_vec[1] > 0:
                direction = np.pi/2
            else:
                direction = -np.pi / 2
        else:
            direction = np.arctan(e_vec[1]/ e_vec[0])
            if e_vec[1] > 0 and e_vec[0] < 0:
                direction = direction + np.pi
            elif e_vec[1] < 0 and e_vec[0] < 0:
                direction = direction - np.pi
        directions.append(direction)
        i += 1
    return directions


def std_deviation_direction(sim):
    directions = get_direction_distribution(sim)
    return np.std(directions)
    
    
def rotate_vec(angle,axis,vec):
    # Rodrigues formula
    # axis of rotation is a unit vector
    #ann-marie code
    vRot = vec*np.cos(angle) + np.cross(axis,vec)*np.sin(angle) + axis*np.dot(axis,vec)*(1 -np.cos(angle))
    return vRot
    
############
# sim variables    #
############

n_particles = 1000
particle_mass = 10000
maxtime = 15000000
timestep = 10000
angle_rotate = np.pi / 100           #angle to rotate vectors through, make bigger for bigger spread in disk
use_uniform = False         #change to false to use normal distribution instead of uniform distribution for rotating angle loop
save_pictures = False       #change to false to skip saving the rebound.OrbitPlot(sim) figure
#collisions = []


def heartbeat_function(sim):
    ps = [p for p in sim.particles if p.id != 0]
    ps = [p for p in ps if p.d <= 1000]
    n_collisions = len(ps)
    if n_collisions > 0:
        for p in ps:
            collisions.append([sim.t, n_collisions, p.d, p.x, p.y, p.z, p.vx, p.vy, p.vz])
        for p in ps:
            sim.remove(id=p.id)

###############
# set up sims              #
###############


aligned = rebound.Simulation()
aligned.units = ('yr', 'au', 'msun')
aligned.add(id=0, m=1.8e8)
i = 1
while i <= n_particles:
    #ann-marie code
    # rotate jhat by angle1 over major axis and angle minor axis
    # rotate ehat by angle2 over minor axis and angle3 about jhat

    ehat = np.array([1,0,0]) 
    jhat = np.array([0,0,1])
    bhat = np.cross(jhat,ehat)

    if use_uniform:
        angle1 = np.random.uniform(-angle_rotate, angle_rotate)
        angle2 = np.random.uniform(-angle_rotate, angle_rotate)
        angle3 = np.random.uniform(-angle_rotate, angle_rotate)
    else:
        angle1 = np.random.normal(0, angle_rotate)
        angle2 = np.random.normal(0, angle_rotate)
        angle3 = np.random.normal(0, angle_rotate)

    jhat = rotate_vec(angle1,ehat,jhat)
    jhat = rotate_vec(angle2,bhat,jhat)
    ehat = rotate_vec(angle2,bhat,ehat)
    ehat = rotate_vec(angle3,jhat,ehat)

    n = np.cross(np.array([0,0,1]), jhat)
    n = n / np.linalg.norm(n)

    Omega_1 = np.arccos(n[0])
    if n[1] < 0:
        Omega_1 = 2*np.pi - Omega_1
    omega_1 = np.arccos(np.dot(n, ehat))
    if ehat[2] < 0:
        omega_1 = 2*np.pi - omega_1

    inclination=np.arccos(jhat[2])
    aligned.add(id=i, m=particle_mass, a=get_a(), e=get_e(), inc = inclination, omega=omega_1, Omega = Omega_1, M=np.random.uniform(0, 2*np.pi))
    i += 1

##################
# integration                      #
##################


i = 0
while i < maxtime:
    aligned.move_to_com()
    aligned.integrate(i)
    #heartbeat_function(aligned)
    if save_pictures:
        alfig = rebound.OrbitPlot(aligned, lim=600000, figsize=(10,10))
        alfig.savefig("run/aligned/" + str(i).zfill(9) + ".png")
        plt.close("all")
        directions = get_direction_distribution(aligned)
        plt.hist(directions)
        plt.savefig("run/directions/" + str(i).zfill(9) + ".png")
    plt.close('all')
    
    #######################
    # take data here                             #
    #######################
    if (i % timestep == 0):
        aligned.save("run/logs/" + str(i).zfill(9) + ".log")
        print(str(int(np.round(i/maxtime*100))) + '%, t=' + str(i))
    i += 10

#pickle.dump(collisions, open("run/collision_logs/collisions.txt", "wb"))
