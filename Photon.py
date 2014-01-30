import numpy as np
import Stat


class Photon(object):
    """Represents a photon in the simulation. Only one photon is ever made, it is just reset when needed"""
    def __init__(self, position, originalAzimuth, originalZenith, wavelength,):
        self.position = position
        #TODO : Compute velocity from original azimuth and zenith angles
        self.velocity = ()
        raise Exception('Construction of photon\'s velocity from azimuth and zenith angle has not been implemented.')
        self.wavelength = wavelength
        self.azimuth = originalAzimuth
        self.zenith = originalZenith
        self.stat = Stat()
        #Some preliminary work for maintaining stat
        #TODO : determine if this should be part of Stat() initialization parameters
        self.stat.wavelength = self.wavelength

    #TODO : decide on deletion or retention
    def specular_reflect(self, record):
        """Update position and velocity of photon for mirror-like reflection off a wall based upon a
                record."""
        self.position += record.time * self.velocity
        self.velocity -= 2 * np.dot(self.velocity, record.normal) * record.normal

    def non_specular_reflect(self, record):
        """Update position and velocity of photon for non-specular reflection off a wall based upon a
                record."""
        raise Exception("non_specular_reflect in Photon.py is not implemented yet.")

    #leaving this here for now but we don't really need it
    #orbit can just do the resetting
    #TODO : decide on deletion or retention
    def reset(self, position, velocity, wavelength):
        """Avoid the costs associated with creating and destroying objects by just resetting the photon
                instead of making a new one"""
        self.position = position
        self.velocity = velocity
        self.wavelength = wavelength