import numpy as np
from Wall import *
import math
from Record import *


class Floor(Wall):
    """Subclass of Wall representing the floor of the simulation"""

    def __init__(self, point1, width):
        """Create a floor with the given point """
        self.point1 = point1
        self.is_boundary = False
        #this tower width + tower pitch
        #TODO: determine if it is safe to assume a square simulation, implement another way to check bounds
        self.width = width
        self.normal = np.array([0, 0, 1])

    def get_collision(self, photon):
        """Override the default behavior of the wall class to determine if their is a collision.
            If there is a collision the proper record is generated, if there is no collision None is returned"""
        # Calculates time and coordinate of collision
        # Discards cases where the photon does not collide with the plane
        if np.dot(photon.velocity, self.normal) == 0:
            raise Exception("I think something broke cause there's a photon moving sideways through the simulation.")
        time = np.dot((self.point1 - photon.position), self.normal) / np.dot(photon.velocity, self.normal)
        if time < 0:
            return None
        intersection = photon.position + (time * photon.velocity)
        # check whether intersection point lies in the square of the simulation
        #if intersection[0] < -self.width or intersection[0] > self.width:
        #    return None
        #if intersection[1] < -self.width or intersection[1] > self.width:
        #    return None
        return Record(self.is_boundary, time, intersection, self.normal, False)