"""Holds the Photon class"""
import numpy as np

class Photon(object):
    """
    Represents a photon in the simulation. Only one photon is ever made, it is just reset when needed

    """

    def __init__(self, position, velocity, wavelength, azimuth, zenith):
        """
        Initialize the photon with the given parameters. Azimuth and Zenith are used to track
        where it initially entered

        @type position: 3D vector, should be numpy array
        @param position: The position of the photon in 3D space
        @type velocity: 3D vector, should be a numpy array
        @param velocity: The velocity of the photon in 3D space
        @type wavelength: floating point number
        @param wavelength: The wavelength of the photon
        @type azimuth: floating point number, radians
        @param azimuth: The initial azimuth angle for this photon
        @type zenith: floating point number, radians
        @param zenith: The initial zentih angle for this photon
        """
        self.position = position
        self.velocity = velocity
        self.wavelength = wavelength
        self.azimuth = azimuth
        self.zenith = zenith

    def specular_reflect(self, record):
        """
        Update position and velocity of photon for a perfect specular
        mirror-like reflection off a wall based upon the given record.
        @type record: Record Object
        @param record: The record to use when performing the reflection
        """
        #
        self.position += record.time * self.velocity
        # v_new = v_old - 2 * <v_old, normal> * normal
        self.velocity -= 2 * np.dot(self.velocity, record.normal) * record.normal

    def wrap_around(self,record):
        """
        Simulate repeating boundary conditions and represent an infinite array by wrapping the photon around to the
        other side
        @type record: Record Object
        @param record: The record to use when performing the wrap around
        """
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
        """
        Update position and velocity of photon for non-specular reflection off a wall based upon a
                record.
        @type record: Record Object
        @param record: The record to use when performing the reflection
                """
        raise NotImplementedError("non_specular_reflect in Photon.py is not implemented yet.")

    #TODO : Implement is_trapped check
    def is_trapped(self, record):
        """See Ricardo for implementation."""
        raise NotImplementedError("is_trapped in Photon.py is not implemented yet.")