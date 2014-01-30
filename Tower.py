import Record
import Cylinder
import Plane
import numpy as np

class Tower(object):
    """Represents a tower in the simulation. Only one tower will be modeled"""

    def __init___(self, height, material, pitch, width,type):
        """Initialize a tower with the given parameters"""
        self.pitch=pitch
        self.material=material
        self.height=height
        self.width=width
        self.walls = []
        #TODO : Construct walls based on height, pitch, width, and material
        #TODO: determine where tower will be centered, there is no position field for tower, will it be centered on origin?
        if type=="cylinder":
            self.walls.append(Cylinder(np.array([0,0]),width))
        elif type=="rectprism":
            self.walls.append(Plane(np.array([-width/2,width/2]),np.array([-width/2,-width/2])))
            self.walls.append(Plane(np.array([-width/2,-width/2]),np.array([width/2,-width/2])))
            self.walls.append(Plane(np.array([width/2,-width/2]),np.array([width/2,width/2])))
            self.walls.append(Plane(np.array([width/2,width/2]),np.array([-width/2,width/2])))



    def get_record(self, photon):
        """Given a photon return the Record corresponding to the first collision"""
        #find the record with the lowest positive time to collision
        record = Record(None, float('inf'), None, None)
        for wall in self.walls:
            temp = wall.get_collision()
            """If this record in invalid, skip it"""
            if temp is None or temp.time <= 0:
                continue
            if temp.time < record.time:
                record = temp
        #return a valid record or None
        return record

