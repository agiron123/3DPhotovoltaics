import Orbit
import math
import numpy as np
import random


class SimpleOrbit(Orbit):
    """A substitute orbit class to use until the actual orbit class is complete.
    Will also be useful for testing the simulation"""
    def __init__(self, rho, zenith, azimuth):
        """Create a simple orbit using the given spherical coordinates"""
        self.rho = rho
        self.zenith = zenith
        self.azimuth = azimuth

    def generate_photon(self, photon, tower):
        """Modify the inputted photon to represent a new photon generated around the given tower.
        Return the modified photon"""
        x = self.rho * math.sin(self.zenith) * math.cos(self.azimuth)
        y = self.rho * math.sin(self.zenith) * math.sin(self.azimuth)
        z = self.rho * math.cos(self.zentih)
        photon.velocity = np.array([x, y, z])
        sim_width = tower.width / 2 + tower.pitch / 2
        epsilon = 10 ** -3
        x = random.uniform(-sim_width, sim_width)
        y = random.uniform(-sim_width, sim_width)
        #TODO: determine what height photons spawn at, shouldn't it be the top, just copying processing code here
        z = tower.height / 2 + epsilon
        photon.position = np.array([x, y, z])
        while photon.position[0] >= -tower.width / 2 and photon.position[0] <= tower.width / 2 \
            and photon.position[1] >= -tower.width/2 and photon.position[1] <= tower.width / 2:
            x = random.uniform(-sim_width, sim_width)
            y = random.uniform(-sim_width, sim_width)
            z = tower.height / 2 + epsilon
            photon.position = np.array([x, y, z])
        photon.wavelength = random.uniform(200, 827)
        return photon

    def step_azimuth(self, delta):
        """Update the Orbit's azimuthal angle by the given delta"""
        self.azimuth += delta
