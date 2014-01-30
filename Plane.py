import Wall
import numpy as np
import Record


class Plane(Wall):

    """Subclass of Wall. Represents a straight line between two points"""
    def __init__(self, point1, point2, material):
        """Create a wall with the given points"""
        self.point1 = point1
        self.point2 = point2
        self.material = material
        #compute normal vector to line formed by the 2 points
        self.normal = np.array([-1, 1]) * (point1-point2)[1::-1]

    #TODO :determine how vectors will be passed around including points, R^2 or R^3 ??
    def get_collision(self, photon):
        """Override the default behavior of the wall class to determine if their is a collision.
            If there is a collision the proper record is generated"""
        time = -sum((photon.position-self.point1)*self.normal) / sum(photon.velocity * self.normal)
        #TODO: check whether intersection lies within the boundaries of the wall
        # TODO : read this cause I'll tell you how write here.  It's easy
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
        """If we are just looking at the plane/line in 2D the time calc above won't work, we can use matrix determinants
        l1=p1+t*v1
        l2=p2+s*v2
        [v1 -v2]*[t s]=p2-p1
        take inverse of 2x2 matrix to solve for s and t, this might be a little slow, but not sure of faster way"""
        intersection = photon.position + time * photon.velocity
        #don't know material, must be set later by tower
        #Or we could ask tower as an __init__ parameter...  Why wait?
        #agreed, we should add material as a field to all wall classes
        return Record(self.material, time, intersection, self.normal)