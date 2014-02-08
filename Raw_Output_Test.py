from Analysis import *
from Statistics import *
from Stat import *
import Photon
import numpy as np
import random

"""This class just test if a Raw data dump works correctly. It does not use all of the functions as they should be used,
    since every required function is not implemented yet. It also just uses random values"""

print("making photon\n")
photon = Photon.Photon(np.array([0, -1, 0]), np.array([1, 1, 0]), 0)
photon.azimuth = random.randint(1, 30) + 0.0
photon.zenith = random.randint(1, 40) + 0.0
photon.wavelength = random.randint(1, 50) + 0.0
print("made photon\n")

print("making stats\n")
stat_list = []
for i in range(100):

    stat = Stat(photon)
    if random.randint(1, 10) % 2 == 0:
        stat.absorbed = False
    else:
        stat.absorbed = True
    if random.randint(1, 10) % 2 == 0:
        stat.trapped = False
    else:
        stat.trapped = True
    stat.path = []
    stat.reflections = random.randint(1, 10) + 0.0
    stat.interactions = random.randint(1, 10) + 0.0

    stat_list.append(stat)
print("made stats\n")

statistic = Statistics()
analysis = Analysis()

print("updating statistic\n")
for stats in stat_list:
    statistic.update(stats)
print("updated statistic\n")

print("outputting data\n")
analysis.generate_output(statistic)
print("outputted data\n")