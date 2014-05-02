"""Holds the Record class"""
class Record(object):
    """Record is used to store information relevant to photon collisions within the simulation"""

    def __init__(self, is_boundary, time, coordinate, normal, is_exiting):
        """
        Create a Record with the given parameters
        @type is_boundary: boolean
        @param is_boundary: Whether this record corresponds to the striking of a boundary
        @type time: floating point number
        @param time: the time of the collision
        @type normal: numpy array, a vector
        @param normal: The normal vector to the point of collision
        @type is_exiting: boolean
        @param is_exiting: Whether this record corresponds to the exiting of a photon
        """
        self.is_boundary = is_boundary
        #time, coordinate, and normal are all relative to the collision point
        self.time = time
        self.coordinate = coordinate
        self.normal = normal
        self.is_exiting = is_exiting
