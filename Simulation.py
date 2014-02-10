from SimpleOrbit import *
from Tower import *
from Photon import *
from Stat import *
from Material import *
from Statistics import *
import random
import math


def run(settings, statistics):
    """Run receives an arguments dictionary from main, this contains all of the relevant information needed to setup
    and run the simulation in the form of key value pairs"""
    #pass relevant arguments to each of these constructor functions, details omitted for now
    #TODO : actually pull from settings here
    i, photon_count, absorbing, trapping, specularOnly = 0, 10000, True, False, True
    orbit = SimpleOrbit(1, math.pi / 2 + math.pi / 4, math.pi / 2 + math.pi / 4)
    photon = Photon(0, 0, 0)
    #CZTS
    material = Material(0.0001, 1.45)
    #TODO: determine proper realtive scaling here, make sure to leverage aspect ratio
    tower = Tower(40, material, 10, 40, "rectprism")
    #TODO : determine what time scale we will use throughout the program
    #t, total_time, delta_t = 0, 10**6, 10
    #outer most loop, we either need to run the simulation for some amount of time
    #or for some distance of orbit, something like that
    while i < photon_count:
        #generate a new photon from orbit
        photon = orbit.generate_photon(photon, tower)
        #generate new stat datum
        stat = Stat(photon)
        done = False
        #check if the photon is outside a tower, not enough going on yet to write this
        #TODO: implement this
        """if tower.contains(photon):
            #TODO : handle photon being spawned at the top of tower
            raise ValueError
            continue"""
        while not done:
            #get a collision
            record = tower.get_record(photon)
            #check 3 things
            #exiting
            if record.is_exiting:
                stat.exit(photon)
                done = True  # move onto next photon
            #wrap around
            elif record.is_boundary:
                stat.wrap_around(photon, record)
                photon.wrap_around(record)
            #absorbed
            elif absorbing and random.random() < 0.1: #tower.material.is_absorbed(photon):
                stat.absorb(photon, record)
                done = True  # move onto next photon
            #trapped
            elif trapping and photon.trapped(record):
                #TODO : do trapping work here
                stat.trap(photon, record)
                #something else?
                break  # move onto next photon
            elif specularOnly:
                photon.specular_reflect(record)
                stat.reflect(photon,record)
            else:
                photon.non_specular_reflect(record)
        #finish with this photon by updating statistics with its stat datum
        statistics.update(stat)
        i += 1
    print(statistics.data["avg_number_interactions"])
run(None, Statistics())