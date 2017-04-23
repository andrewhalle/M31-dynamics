import sys
import rebound
import numpy as np
import matplotlib as mpl
mpl.use('Agg') #only use this when computing on server
import matplotlib.pyplot as plt
import pickle
from random import random

#########################################
#  convenience functions and classes    #
#########################################

def get_a():
    x = np.random.uniform(1, 2)
    y = np.random.uniform(0, 1)
    fx = x**(-1)
    if y < fx:
        return x
    else:
        return get_a()

def get_e():
    e = np.random.normal(loc=0.6, scale=0.1)
    if e > 0 and e < 1:
        return e
    return get_e()
    
def rotate_vec(angle,axis,vec):
    # Rodrigues formula
    # axis of rotation is a unit vector
    #ann-marie code
    vRot = vec*np.cos(angle) + np.cross(axis,vec)*np.sin(angle) + axis*np.dot(axis,vec)*(1 -np.cos(angle))
    return vRot

def textMe():
    from twilio.rest import TwilioRestClient
    account_sid = "AC2f1cf577fbea080a7aa8f3aa7a296560"
    auth_token = "f4bc56655d8a11b576d01fb2d666b7cd"
    client = TwilioRestClient(account_sid, auth_token)
    message = client.messages.create(body="Simulation " + str(sim_number) + "finished", to="+19256403336", from_="+19259058442")
    
####################
# sim variables    #
####################

sim_number = sys.argv[1]
n_particles = 100
particle_mass = 1e-4
disruption_limit = 1e-2
soften = 1e-6
maxtime = 10000
timestep = 20
angle_rotate = np.pi / 100           #angle to rotate vectors through, make bigger for bigger spread in disk
use_uniform = False         #change to false to use normal distribution instead of uniform distribution for rotating angle loop
collision_events = []       #[id, [time], [x], [y], [z], [vx], [vy], [vz]]
active_collision_events = []
initial_e = 0.1  #originally random() for suite of simulations


def heartbeat_function(sim):
    ps = [p for p in sim.particles if (p.id != 0 and p.d < disruption_limit)]
    new_cols = [p for p in ps if (p.id not in [a[0] for a in active_collision_events])]
    continuing_cols = [p for p in ps if (p.id in [a[0] for a in active_collision_events])]
    finished_cols = [col for col in active_collision_events if col[0] not in [p.id for p in ps]]
    for col in new_cols:
        active_collision_events.append([col.id, [sim.t], [col.x], [col.y], [col.z], [col.vx], [col.vy], [col.vz]])
    for col in continuing_cols:
        active_collision_event = [a for a in active_collision_events if a[0] == col.id][0]
        active_collision_event[1].append(sim.t)
        active_collision_event[2].append(col.x)
        active_collision_event[3].append(col.y)
        active_collision_event[4].append(col.z)
        active_collision_event[5].append(col.vx)
        active_collision_event[6].append(col.vy)
        active_collision_event[7].append(col.vz)
    for col in finished_cols:
        collision_events.append(col)
        active_collision_events.remove(col)

###############
# set up sims #
###############


unaligned = rebound.Simulation()
unaligned.add(id=0, m=1)
unaligned.softening = soften
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
    #changed to flat e distribution
    unaligned.add(id=i, m=particle_mass, a=get_a(), e=initial_e, inc = 0, omega=np.random.uniform(0, 2*np.pi), Omega = np.random.uniform(0, 2*np.pi), M=np.random.uniform(0, 2*np.pi))
    i += 1

##################
# integration    #
##################

unaligned.move_to_com()
i = 0
while i < maxtime:
    unaligned.integrate(i)
    unaligned.move_to_com()
    heartbeat_function(unaligned)
    #######################
    # take data here      #
    #######################
    if (i % timestep < 0.001 or i % timestep > timestep - 0.001):
        unaligned.save("logs/suite/unaligned/" + sim_number + "/" + str(int(i)).zfill(9) + ".log")
        print(str(int(np.round(i/maxtime*100))) + '%, t=' + str(i))
    i += 0.1
    print(i)

pickle.dump(collision_events, open("logs/suite/unaligned/" + sim_number + "/collision_events.txt", "wb"))
#textMe() - twilio account no longer active
