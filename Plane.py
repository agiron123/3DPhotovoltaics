import numpy as np
from Record import *
import math


class Plane(object):
    """Subclass of Wall. Represents a plane"""
    def __init__(self, point1, point2, is_boundary):
        """Create a plane with the given points"""
        self.point1 = point1
        self.point2 = point2
        self.is_boundary = is_boundary
        #compute normal vector to line formed by the 2 points, assuming points have no z component
        normal = np.cross(np.array([0, 0, 1]), (self.point2 - self.point1))
        self.normal = normal / math.sqrt(np.dot(normal, normal))

    def get_collision(self, photon):
        """Override the default behavior of the wall class to determine if their is a collision.
            If there is a collision the proper record is generated if there is no collision None is returned"""
        """Define intersection as the weighted sum of point1 and point2
            Check if the two sums add up to one and are both positive.
            To cut down on the math and such, defined one weight as (s) and the other as (1-s),
                then check both s is between 0 and 1.
                s*point1 + (1-s)*point2 == intersection
                s*(point1-point2) + point2 == intersection
                s = (intersection - point2) / (point1 - point2)
                @walker, this looks makes sense up until here, how can you divide two vectors, or am I missing something obvious? p1 and p2 are vectors right?
                if s < 0 or s > 1:
                    return None"""
        # Calculates time and coordinate of collision
        # Discards cases where the photon does not collide with the plane
        if np.dot(photon.velocity, self.normal) == 0:
            return None
        time = np.dot((self.point1 - photon.position), self.normal) / np.dot(photon.velocity, self.normal)
        if time < 0:
            return None
        intersection = photon.position + (time * photon.velocity)

        """I think this method works better, I don't understand what the vector division above represents but what I have below should work
        and is definitely mathematically rigorous, let int be intersection
        s*(p2 - p1) + p1 = int
        s*(p2 - p1) = (int - p1) , take magnitude of each side
        <s*(p2 - p1), s*(p2 - p1)> = <(int - p1), (int - p1)>
        s^2 <(p2 - p1), (p2 - p1)> = <(int - p1), (int - p1)>
        s^2 = <(int - p1), (int - p1> / <(p2 - p1), (p2 - p1)>
        """
        """
        s = math.sqrt(np.dot(ai, ai) / np.dot(ab, ab))
            """
        # Discards collisions that collides with the plane outside the bounds of the wall
        ab = self.point2 - self.point1
        if math.fabs(ab[0]) > math.fabs(ab[1]):
            s = (intersection[0] - self.point1[0]) / ab[0]
        else:
            s = (intersection[1] - self.point1[1]) / ab[1]
        if s < 0 or s > 1:
            return None
        return Record(self.is_boundary, time, intersection, self.normal, False)