import Wall
import numpy as np
import Record


class Plane(Wall):

    """Subclass of Wall. Represents a straight line between two points"""
    def __init__(self, point1, point2):
        """Create a wall with the given points"""
        self.point1 = point1
        self.point2 = point2
        #compute normal vector too line formed by the 2 points
        self.normal = np.array([-1,1])*(point1-point2)[1::-1]
    #TODO :determine how vectors will be passed around including points, R^2 or R^3 ??
    def get_collision(self, photon):
        """Override the default behavior of the wall class to determine if their is a collision.
            If there is a collision the proper record is generated"""
        time=-sum((photon.position-self.point1)*self.normal)/sum(photon.velocity*self.normal)
        #TODO: check whether intersection lies within the boundaries of the wall
        intersection=photon.position+time*photon.velocity
        #don't know material, must be set later by tower
        return Record(None,time,intersection,self.normal)