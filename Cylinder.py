from Record import *
import numpy as np
import math

class Cylinder(object):
    """Subclass of wall. Represents a circle"""
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
        #TODO : implement me
        #This is correct, but the first line is unclear, can't multiply vectors
        #we are solving this, P=photon C=circle
        #<P.p + t*P.V - C.p , P.p + t*P.v - C.p> = r^2, math works out the same
        # How to implement:
        #       Solve (CP + t*V)^2 == radius^2 in 2D
        #       (CP + t*V) * (CP + t*V) == radius^2
        #       dot(CP,CP) + 2*t*dot(V,CP) + t*t*dot(V,V) == radius^2
        #       solve quadratic equation a*t^2 + b*t + c = 0 for
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
        #TODO: Confirm this line, shouldn't it be intersection= photon.position+ (time * photon.velocity)
        intersection = photon.position + (time * photon.velocity)
        normal = intersection - self.center
        normal[2] = 0.0
        unit_normal = normal / math.sqrt(np.dot(normal, normal))
        # TODO: Confirm this, why are you doing cos and sin stuff the unit vector above is normal to the circle at the point of intersection shouldn't we just use that
        #theta = math.atan2(unit_vector.y, unit_vector.x)
        #normal = (math.cos(theta), math.sin(theta), 0)
        return Record(self.is_boundary, time, intersection, unit_normal, False)