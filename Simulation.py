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
    i, photon_count, absorbing, trapping, specular_only = 0, 1000, False, False, True
    ignore_tower_tops = True
    #orbit = SimpleOrbit(1, math.pi / 2.0 - math.pi / 4.0, math.pi / 2.0)
    orbit = SimpleOrbit(1, settings["zenith"], settings["azimuth"])
    photon = Photon(0, 0, 0, 0, 0)
    #ignoring absorptions
    material = None
    tower = Tower(settings["height"], material, settings["spacing"], settings["width"], "rectprism")
    while i < photon_count:
        #generate a new photon from orbit
        photon = orbit.generate_photon(photon, tower)
        #generate new stat datum
        stat = Stat(photon)
        done = False
        if tower.includes(photon):
            if not ignore_tower_tops:
                done = True
                record = Record(False, 0, photon.position, np.array([0, 0, 1]), True)
                if absorbing and tower.material.is_absorbed(photon):
                    stat.absorb(photon, record)
                elif trapping and photon.is_trapped():
                    stat.trap(photon, record)
                else:
                    stat.reflect(photon, record)
            else:
                #completely ignore photons spawned on the top of the tower
                continue
        #continue until photon is absorbed, trapped, or exits the simulation
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
            elif absorbing and tower.material.is_absorbed(photon):
                stat.absorb(photon, record)
                done = True  # move onto next photon
            #trapped
            elif trapping and photon.trapped(record):
                #TODO : do trapping work here
                stat.trap(photon, record)
                #something else?
                done = True  # move onto next photon
            elif specular_only:
                photon.specular_reflect(record)
                stat.reflect(photon, record)
            else:
                photon.non_specular_reflect(record)
        #finish with this photon by updating statistics with its stat datum
        statistics.update(stat)
        i += 1
    return statistics.data["avg_number_interactions"]