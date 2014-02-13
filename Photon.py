import numpy as np


class Photon(object):
    """Represents a photon in the simulation. Only one photon is ever made, it is just reset when needed"""
    def __init__(self, position, velocity, wavelength, azimuth, zenith):
        self.position = position
        self.velocity = velocity
        self.wavelength = wavelength
        self.azimuth = azimuth
        self.zenith = zenith

    def specular_reflect(self, record):
        """Update position and velocity of photon for mirror-like reflection off a wall based upon a
                record."""
        self.position += record.time * self.velocity
        self.velocity -= 2 * np.dot(self.velocity, record.normal) * record.normal

    def wrap_around(self,record):
        self.position += record.time * self.velocity
        #reflect the position around the x or y axis to move to the other side of the simulation
        #left and right boundaries
        if record.normal[1] == 0:
            self.position[0] *= -1
        #top and bottom boundaries
        else:
            self.position[1] *= -1

    #TODO : Implement non-specular reflection
    def non_specular_reflect(self, record):
        """Update position and velocity of photon for non-specular reflection off a wall based upon a
                record."""
        raise NotImplementedError("non_specular_reflect in Photon.py is not implemented yet.")

    #TODO : Implement is_trapped check
    def is_trapped(self, record):
        """See Ricardo for implementation."""
        raise NotImplementedError("is_trapped in Photon.py is not implemented yet.")