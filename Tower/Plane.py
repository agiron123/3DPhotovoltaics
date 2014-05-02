"""Holds the Plane class"""
import math
import numpy as np
from Simulation.Record import *
from Wall import *


class Plane(Wall):
    """
    Subclass of Wall. Represents a plane
    """
    def __init__(self, point1, point2, is_boundary):
        """
        Create a plane with the given points
        @type point1: 3D vector, numpy array
        @param point1: One point defining the plane
        @type point2: 3D vector, numpy array
        @param point2: Another point defining the plane
        @type is_boundary: boolean
        @param is_boundary: Whether the plane is a boundary or not
        """
        self.point1 = point1
        self.point2 = point2
        self.is_boundary = is_boundary
        #compute normal vector to line formed by the 2 points, assuming points have no z component
        normal = np.cross(np.array([0, 0, 1]), (self.point2 - self.point1))
        self.normal = normal / math.sqrt(np.dot(normal, normal))

    def get_collision(self, photon):
        """
        Override the default behavior of the wall class to determine if their is a collision.
        If there is a collision the proper record is generated if there is no collision None is returned
        @type photon: Photon object
        @param photon: The photon to use in determining a collision.
        @rtype: Record Object
        @return: Record summarizing the results of a collision or None if no collision
        """
        # Calculates time and coordinate of collision
        # Discards cases where the photon does not collide with the plane
        if np.dot(photon.velocity, self.normal) == 0:
            return None
        #Derived from this equation <point1 - (photon.position + t * photon.velocity), normal> = 0
        time = np.dot((self.point1 - photon.position), self.normal) / np.dot(photon.velocity, self.normal)
        if time < 0:
            return None
        intersection = photon.position + (time * photon.velocity)
        # Discards collisions that collides with the plane outside the bounds of the wall
        #Derived from this equation s*(point1 - point2) + point2 = intersection
        ab = self.point2 - self.point1
        if math.fabs(ab[0]) > math.fabs(ab[1]):
            s = (intersection[0] - self.point1[0]) / ab[0]
        else:
            s = (intersection[1] - self.point1[1]) / ab[1]
        if s < 0 or s > 1:
            return None
        return Record(self.is_boundary, time, intersection, self.normal, False)