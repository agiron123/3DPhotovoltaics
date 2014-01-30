import Wall
import numpy as np

class Circle(Wall):
    """Subclass of wall. Represents a circle"""
    def __init__(self, center, radius):
        """Create a circle with the given center and radius
        :param center: The center of the circle.
        :param radius: The radius of the circle.
        """
        self.center = center
        self.radius = radius

    def get_collision(self):
        """Override the default behavior of the wall class to determine if their is a collision.
            If there is a collision the proper record is generated"""
        #TODO : implement me
        """How to implement:
                Solve (CP + t*V)^2 == radius^2 in 2D
                (CP + t*V) * (CP + t*V) == radius^2
                dot(CP,CP) + 2*t*dot(V,CP) + t*t*dot(V,V) == radius^2
                solve quadratic equation a*t^2 + b*t + c = 0 for
                a = dot(V,V)
                b = 2*dot(V,CP)
                c = dot(CP,CP) - radius^2
                where CP = photon.position - self.center
                      V = photon.velocity

                return record with lowest real t-value or None if no solution exists
                NOTE: These are 2D dot products"""
        raise Exception('Circle collision is not implemented yet')