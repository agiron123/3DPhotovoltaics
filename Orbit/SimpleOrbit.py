"""Contains class for a simple orbit. In this orbit the sun is a point source"""
from Orbit import *
import math
import numpy as np
import random


class SimpleOrbit(Orbit):
    """A substitute orbit class to use until the actual orbit class is complete.
    Will also be useful for testing the simulation. This simple orbit treats the sun as a point source located
    at the given spherical coordinates"""
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
        z = self.rho * math.cos(self.zenith)
        photon.velocity = np.array([x, y, z])
        photon.velocity *= -1
        sim_width = tower.width / 2 + tower.pitch / 2
        x = random.uniform(-sim_width, sim_width)
        y = random.uniform(-sim_width, sim_width)
        z = tower.height / 2
        photon.position = np.array([x, y, z])
        photon.wavelength = random.uniform(200, 827)
        photon.azimuth = self.azimuth
        photon.zenith = self.zenith
        return photon

    def step_azimuth(self, delta):
        """Update the Orbit's azimuthal angle by the given delta"""
        self.azimuth += delta
