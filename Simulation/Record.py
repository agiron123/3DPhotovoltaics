"""Holds the Record class"""
class Record(object):
    """Record is used to store information relevant to photon collisions within the simulation"""

    def __init__(self, is_boundary, time, coordinate, normal, is_exiting):
        """Create a Record with the given parameters"""
        self.is_boundary = is_boundary
        #time, coordinate, and normal are all relative to the collision point
        self.time = time
        self.coordinate = coordinate
        self.normal = normal
        self.is_exiting = is_exiting
