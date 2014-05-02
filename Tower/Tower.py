"""Holds the Tower class"""
from Cylinder import *
from Plane import *
from Floor import *


class Tower(object):
    """
    Represents a tower in the simulation. Only one tower will be modeled.
    The Tower is always centered on the origin
    """
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
        """
        Initialize a tower with the given parameters
        @type height: floating point number
        @param height: The tower's height
        @type material: Material Object
        @param material: The material the tower is coated with
        @type pitch: floating point number
        @param pitch: How far the towers are spaced apart
        @type width: floating point number
        @param width: The tower's width
        @type tower_type: string, should match preset values
        @param tower_type: the shape of the tower, must be from preset list of values
        """
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
        """
        Given a photon return the Record corresponding to the first collision. If there is no collision Record's
        is_exiting field will be true and all other fields will be None or infinity
        @type photon: Photon object
        @param photon: the photon to determine a collision for
        @rtype: Record Object
        @return: The calculated Record, will indicate a collision, a wrap around, or exiting, contains all needed info
        """
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
        """
        Determine whether the given photon is on the top of the tower. Note that by inside
        we really mean whether it is over the tower or not (i.e. inside its 2D bounds)
        @type photon: Photon object
        @param photon: The photon in questions
        @rtype: boolean
        @return: Whether the photon is inside the tower or not

        """
        #for any of these shapes we can just take the dot product with each wall
        #all of the signs will match if the photon is "inside" the tower
        #note this assumes we are consistent with our normal vectors, which we are
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
        """
        Utility method for is inside method, we just do the dot product and copy the sign
        @type photon: Photon Object
        @param photon: The photon in questions
        @rtype: floating point number
        @return: The sign copied result of the dot product operation
        """
        return math.copysign(1.0, np.dot(wall.normal, photon.position - wall.point1))