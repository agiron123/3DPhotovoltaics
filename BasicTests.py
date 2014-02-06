from Photon import *
import numpy as np
from random import *
from Plane import *
from Cylinder import *
from Tower import *

"""These are just some very basic tests I ran will I was writing stuff"""
#really basic tests, should collide and reflect simply
a = np.array([0, 0, 0])
photon = Photon(np.array([0, -1, 0]), np.array([1, 1, 0]), 0)
wall = Plane(np.array([1, 5, 0]), np.array([1, -5, 0]), False)
r = wall.get_collision(photon)
print (r.normal)
print(r.coordinate, r.time)
photon.specular_reflect(r)
print(photon.position, photon.velocity)

#should not collide
photon = Photon(np.array([0, 10, 0]), np.array([1, 1, 0]), 0)
wall = Plane(np.array([1, 1, 0]), np.array([1, -1, 0]), False)
r = wall.get_collision(photon)
print (r)


#should collide and reflect simply
photon = Photon(np.array([0, 0, 0]), np.array([1, 0, 0]), 0)
circle = Cylinder(np.array([5, 0, 0]), 1, False)
r = circle.get_collision(photon)
print(r.normal)
print(r.coordinate, r.time)
photon.specular_reflect(r)
print(photon.position, photon.velocity)

#should not collide
photon = Photon(np.array([0, 0, 0]), np.array([0, 100, 0]), 0)
circle = Cylinder(np.array([5, 0, 0]), 1, False)
r = circle.get_collision(photon)
print(r)


#should collide and reflect back and up
photon = Photon(np.array([0, -3, 0]), np.array([1, 1, 0]), 0)
circle = Cylinder(np.array([4, 0, 0]), 1, False)
r = circle.get_collision(photon)
print(r.normal)
print(r.coordinate, r.time)
photon.specular_reflect(r)
print(photon.position, photon.velocity)


#set up a tower, and test part of simulations main loop
photon = Photon(np.array([-7, 0, 5]), np.array([1, 0, 0]), 0)
tower = Tower(10, None, 10, 10, "rectprism")
done = False
reflections = 0
while not done and 'y'==raw_input("continue?"):
    #get a collision
    record = tower.get_record(photon)
    #check 3 things
    #exiting
    if record.is_exiting:
        done = True  # move onto next photon
    #wrap around
    elif record.is_boundary:
        photon.wrap_around(record)
        print("wrapped around, info is",photon.position, photon.velocity)
    #absorbed
    elif random() < .1:
        done = True  # move onto next photon
    else:
        photon.specular_reflect(record)
        reflections += 1
        print("reflected, info is",photon.position, photon.velocity)
print(reflections)

#set up another tower, and test part of simulations main loop
photon = Photon(np.array([-7, 0, 8]), np.array([1, 0, -1]), 0)
tower = Tower(10, None, 10, 10, "rectprism")
done = False
reflections = 0
while not done:
    #get a collision
    record = tower.get_record(photon)
    #check 3 things
    #exiting
    if record.is_exiting:
        done = True  # move onto next photon
    #wrap around
    elif record.is_boundary:
        photon.wrap_around(record)
    #absorbed
    elif random() < .1:
        done = True  # move onto next photon
    else:
        photon.specular_reflect(record)
        reflections += 1
print(reflections)

#test the ground directly
photon = Photon(np.array([-7, 0, 8]), np.array([0, 0, -1]), 0)
tower = Tower(10, None, 10, 10, "rectprism")
record = tower.get_record(photon)
print(record.coordinate, record.time)
photon.specular_reflect(record)
print(photon.position, photon.velocity)
record = tower.get_record(photon)
print(record.is_exiting)