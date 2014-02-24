from Record import *
from Cylinder import *
from Plane import *
from Floor import *
import numpy as np


class Tower(object):
    """Represents a tower in the simulation. Only one tower will be modeled.
    The Tower is always centered on the origin"""
    #constants
    epsilon = 10 ** -7
    RECT_PRISM = "rect_prism"
    CYLINDER = "cylinder"
    CONVEX_POLYGON = "convex_polygon"
    #infinite in x direction
    YTRENCH = "ytrench"
    #infinite in y direction
    XTRENCH = "xtrench"
    BOX = "box"

    def __init__(self, height, material, pitch, width, tower_type):
        """Initialize a tower with the given parameters"""
        self.pitch = pitch
        self.material = material
        self.height = height
        self.width = width
        self.tower_type = tower_type
        #this wall list contains a list of walls forming both the tower and its boundaries
        #walls are created using points in counter clockwise order
        self.walls = []
        #boundaries
        d = pitch / 2 + width / 2
        s = width / 2
        self.walls.append(Plane(np.array([-d, d, 0]), np.array([-d, -d, 0]), True))
        self.walls.append(Plane(np.array([-d, -d, 0]), np.array([d, -d, 0]), True))
        self.walls.append(Plane(np.array([d, -d, 0]), np.array([d, d, 0]), True))
        self.walls.append(Plane(np.array([d, d, 0]), np.array([-d, d, 0]), True))
        #add a floor
        self.walls.append(Floor(-height/2.0))
        #add walls specific to the given type
        if tower_type == Tower.CYLINDER:
            self.walls.append(Cylinder(np.array([0, 0, 0]), s, False))
        #trench is infinite in the y direction
        elif tower_type == Tower.XTRENCH:
            self.walls.append(Plane(np.array([-s, d, 0]), np.array([-s, -d, 0]), False))
            self.walls.append(Plane(np.array([s, -d, 0]), np.array([s, d, 0]), False))
        #trench is infinite in the x direction
        elif tower_type == Tower.YTRENCH:
            self.walls.append(Plane(np.array([d, s, 0]), np.array([-d, s, 0]), False))
            self.walls.append(Plane(np.array([-d, -s, 0]), np.array([d, -s, 0]), False))
        #distinguised by is inside method
        elif tower_type == Tower.RECT_PRISM:
            self.walls.append(Plane(np.array([-s, s, 0]), np.array([-s, -s, 0]), False))
            self.walls.append(Plane(np.array([-s, -s, 0]), np.array([s, -s, 0]), False))
            self.walls.append(Plane(np.array([s, -s, 0]), np.array([s, s, 0]), False))
            self.walls.append(Plane(np.array([s, s, 0]), np.array([-s, s, 0]), False))
        elif tower_type == Tower.BOX:
            self.walls.append(Plane(np.array([-d + s, d - s, 0]), np.array([-d + s, -d + s, 0]), False))
            self.walls.append(Plane(np.array([-d + s, -d + s, 0]), np.array([d - s, -d + s, 0]), False))
            self.walls.append(Plane(np.array([d - s, -d + s, 0]), np.array([d - s, d - s, 0]), False))
            self.walls.append(Plane(np.array([d - s, d - s, 0]), np.array([-d + s, d - s, 0]), False))
        else:
            raise NotImplementedError("The specified wall type is not currently supported")

    def get_record(self, photon):
        """Given a photon return the Record corresponding to the first collision. If there is no collision Record's
            is_exiting field will be true and all other fields will be None or infinity"""
        #find the record with the lowest positive time to collision
        record = Record(False, float('inf'), None, None, True)
        for wall in self.walls:
            temp = wall.get_collision(photon)
            #If this record in invalid, skip it
            if temp is None or temp.time <= Tower.epsilon:
                continue
            if temp.time < record.time:
                record = temp
        #no collisions, exiting
        if record.coordinate is None:
            return record
        #a collision occurred above the tower's height, flag this as exiting
        elif record.coordinate[2] > self.height / 2.0:
            record = Record(False, float('inf'), None, None, True)
        #return a valid record
        return record

    def is_inside(self, photon):
        """Determine whether the given photon is on the top of the tower"""
        if self.tower_type == Tower.CONVEX_POLYGON or self.tower_type == Tower.YTRENCH or \
            self.tower_type == Tower.RECT_PRISM or self.tower_type == Tower.XTRENCH:
            base_orientation = Tower.wall_normal_dot(self.walls[0], photon)
            for wall in self.walls:
                if base_orientation != Tower.wall_normal_dot(wall, photon):
                    return False
            return True
        elif self.tower_type == Tower.CYLINDER:
            copy = photon.position.copy()
            copy[2] = 0
            return np.dot(copy, copy) <= self.width * self.width
        elif self.tower_type == Tower.BOX:
            base_orientation = Tower.wall_normal_dot(self.walls[0], photon)
            for wall in self.walls:
                if base_orientation != Tower.wall_normal_dot(wall, photon):
                    return True
            return False
        else:
            raise NotImplementedError("Unsupported tower shape")

    @staticmethod
    def wall_normal_dot(wall, photon):
        return math.copysign(1.0, np.dot(wall.normal, photon.position - wall.point1))