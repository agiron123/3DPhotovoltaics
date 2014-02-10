import math
import numpy as np
import random
from Photon import *

class Orbit(object):
    """Represents the orbit of the ISS in space.
        Is responsible for generating an accurate probability distribution
        of intial photon parameters (i.e. velocity, wavelength, and position). Is also responsible for
        determining how many photons will be fired per time step."""

    def __init__(self):
        """Initialize the orbit given the initial parameters"""
        #not sure what exactly to put here right now, we need a better understanding of the physics
        #to determine that exactly, beta angles, and earth shine definitely seem like things which should go here

    #attempt at porting the generate_photon method from Christian's processing code to use as a dummy generate photon for now
    def dummy_generate_photon(self,photon,tower):
        azimuth=photon.azimuth*math.PI/180;
        rho=1
        #TODO: make sure we are using proper angles, different conventions on order in which zenith and azimuth angles are listed and such
        velocity=np.array([rho*math.sin(zenith)*math.cos(azimuth),rho*math.sin(zenith)*math.sin(azimuth),rho*math.cos(zenith)])
        simWidth=tower.width/2+tower.pitch/2
        epsilon=10**-2
        #random x and y between boundaries, slightly different from processing code, need to confirm correctness
        position=np.array([random.uniform(-simWidth,simWidth),random.uniform(-simWidth,simWidth),tower.height-epsilon])
        wavelength=random.uniform(200,827)
        #TODO: determine whether photon will be updated or whether we will return a new photon
        #TODO: need to determine where zenith, and azimuth will be stored, also need to determine where velocity will be calculated i think photon is a bad place
        #do we need a while loop like in processing code to determine if this photon is valid?
        #pass stuff to constructor here
        return Photon()


    def generate_photon(self, photon, tower):
        """Reset the photon which the simulation is using to represent a new photon"""
        #TODO : hard physics stuff goes here
        #NOTE : leaving a normal distribution here
        #TODO: do we want a normal distribution here or the distribution from the processing code


    def time_step(self, delta_t):
        #TODO: seems like for release one we could update zenith and azimuth here
        """Move the ISS along the orbit by the given time step. The probability distribution of
            generate_photon will reflect this change"""