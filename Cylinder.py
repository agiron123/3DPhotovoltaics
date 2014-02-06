import Wall
import Record
import numpy as np
import math

class Cylinder(object):
    """Subclass of wall. Represents a circle"""
    def __init__(self, center, radius, material):
        """Create a circle with the given center and radius
        :param center: The center of the circle.
        :param radius: The radius of the circle.
        """
        self.center = center
        self.radius = radius
        self.material = material

    def get_collision(self, photon):
        """Override the default behavior of the wall class to determine if their is a collision.
            If there is a collision the proper record is generated"""
        #TODO : implement me
        # How to implement:
        #       Solve (CP + t*V)^2 == radius^2 in 2D
        #       (CP + t*V) * (CP + t*V) == radius^2
        #       dot(CP,CP) + 2*t*dot(V,CP) + t*t*dot(V,V) == radius^2
        #       solve quadratic equation a*t^2 + b*t + c = 0 for
        # Pre-processes for a vector
        CP = photon.position - self.center
        CP.z = 0
        V = photon.velocity.copy()
        V.z = 0

        # Sets up quadratic system to find time to collision with cylinder
        a = np.dot(V, V)
        b = 2.0 * np.dot(V, CP)
        c = np.dot(CP, CP) - self.radius * self.radius
        determinant = b * b - 4 * a * c

        # Determines which collision occurs first using the smallest positive time
        # Discards invalid collisions
        time = float("inf")
        if determinant < 0:
            return Record(None, time, None, None)
        time1 = (-b + determinant) / (2 * a)
        time2 = (-b - determinant) / (2 * a)
        if time1 < 0 and time2 < 0:
            return Record(None, time, None, None)
        elif time1 < 0:
            time = time2
        elif time2 < 0:
            time = time1
        elif time1 < time2:
            time = time1
        else:
            time = time2

        # Computes Record for the first valid collision with the Cylinder wall
        intersection = CP + (time * photon.velocity)
        unit_vector = intersection - self.center
        theta = math.atan2(unit_vector.y, unit_vector.x)
        normal = (math.cos(theta), math.sin(theta), 0)
        return Record(self.material, time, intersection, normal)
