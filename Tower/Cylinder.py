import math

import numpy as np

from Simulation.Record import *
from Wall import *


class Cylinder(Wall):
    """Subclass of wall. Represents a Cylinder"""
    def __init__(self, center, radius, is_boundary):
        """Create a circle with the given center and radius
        :param center: The center of the circle.
        :param radius: The radius of the circle.
        """
        self.center = center
        self.radius = radius
        self.is_boundary = is_boundary

    def get_collision(self, photon):
        """Override the default behavior of the wall class to determine if their is a collision.
            If there is a collision the proper record is generated. If there is no collision None is returned"""
        #Derived from this equation, P=photon C=circle
        #<P.position + t * P.velocity - C.center , P.position + t * P.velocity - C.center> = C.radius^2
        #cp = P.position - C.center
        #<cp, cp> + 2 * t * <v, cp> + t^2 * <v,v> == C.radius^2, just solve quadratic from here
        cp = photon.position - self.center
        cp[2] = 0
        v = photon.velocity.copy()
        v[2] = 0

        # Sets up quadratic system to find time to collision with cylinder
        a = np.dot(v, v)
        b = 2.0 * np.dot(v, cp)
        c = np.dot(cp, cp) - self.radius * self.radius
        determinant = b * b - 4 * a * c

        # Determines which collision occurs first using the smallest positive time
        # Discards invalid collisions
        time = float("inf")
        if determinant < 0:
            return None
        time1 = (-b + math.sqrt(determinant)) / (2 * a)
        time2 = (-b - math.sqrt(determinant)) / (2 * a)
        if time1 < 0 and time2 < 0:
            return None
        elif time1 < 0:
            time = time2
        elif time2 < 0:
            time = time1
        elif time1 < time2:
            time = time1
        else:
            time = time2

        # Computes Record for the first valid collision with the Cylinder wall
        intersection = photon.position + (time * photon.velocity)
        normal = intersection - self.center
        normal[2] = 0.0
        unit_normal = normal / math.sqrt(np.dot(normal, normal))
        return Record(self.is_boundary, time, intersection, unit_normal, False)
