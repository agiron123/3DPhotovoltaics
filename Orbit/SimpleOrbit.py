"""Contains class for a simple orbit. In this orbit the sun is a point source"""
from Orbit import *
import math
import numpy as np
import random


class SimpleOrbit(Orbit):
    """
    A substitute orbit class to use until the actual orbit class is complete.
    Will also be useful for testing the simulation. This simple orbit treats the sun as a point source located
    at the given spherical coordinates
    """
    def __init__(self, rho, zenith, azimuth):
        """
        Create a simple orbit using the given spherical coordinates
        @type rho: should always be 1 for now
        @param rho: not currently used, should always be 1 for now
        @type zenith: floating point number, radians
        @param zenith: the zenith angle for the point source sun in polar coordinates
        @type azimuth: floating point number, radians
        @param azimuth: the azimuth angle for the point source sun in polar coordinates
        """
        self.rho = rho
        self.zenith = zenith
        self.azimuth = azimuth

    def generate_photon(self, photon, tower):
        """
        Modify the inputted photon to represent a new photon generated around the given tower.
        Return the modified photon
        @type photon: Photon object
        @param photon: The photon which is being modified into a new photon
        @type tower: A Tower Object
        @param tower: The tower to use for determining the photons starting position (need the bounds of the simulation)
        @rtype: Photon object
        @return: The new photon which was created by this orbit (actually just the old photon updated)
        """
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
        """
        Update the Orbit's azimuthal angle by the given delta
        @type delta: floating point number
        @param delat: how much to step the azimuth angle by
        """
        self.azimuth += delta
