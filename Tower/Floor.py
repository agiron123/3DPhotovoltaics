import numpy as np
from Wall import *
from Simulation.Record import *


class Floor(Wall):
    """Subclass of Wall representing the floor of the simulation"""

    def __init__(self, depth):
        """Create a floor with the given depth """
        self.point1 = np.array([0, 0, -depth])
        self.depth = depth
        self.is_boundary = False
        self.normal = np.array([0, 0, 1])

    def get_collision(self, photon):
        """Override the default behavior of the wall class to determine if their is a collision.
            If there is a collision the proper record is generated, if there is no collision None is returned"""
        # Calculates time and coordinate of collision
        # Discards cases where the photon does not collide with the plane
        if np.dot(photon.velocity, self.normal) == 0:
            raise Exception("I think something broke cause there's a photon moving sideways through the simulation.")
        #Derived from this equation <point1 - (photon.position + t * photon.velocity), normal> = 0
        time = (photon.position[2]-self.depth) / (-photon.velocity[2])
        if time < 0:
            return None
        intersection = photon.position + (time * photon.velocity)
        return Record(self.is_boundary, time, intersection, self.normal, False)