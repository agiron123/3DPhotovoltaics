import Wall
import numpy as np


class Line(Wall):

    """Subclass of Wall. Represents a straight line between two points"""
    def __init__(self,point1,point2):
        """Create a wall with the given points"""
        self.point1=point1
        self.point2=point2
        #compute normal vector too line formed by the 2 points
        self.normal=np.array([-1,1])*(point1-point2)[1::-1]

    def get_collision(self,photon):
        """Override the default behavior of the wall class to determine if their is a collision.
            If there is a collision the proper record is generated"""
        return None