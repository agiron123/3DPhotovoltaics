class Record(object):
    """Record is used to store information relevant to photon collisions within the simulation"""

    def __init__(self, is_boundary, time, coordinate, normal, is_exiting):
        """Create a Record with the given parameters"""
        #this is good, avoid using null as a flag and use this boolean field instead
        self.is_boundary = is_boundary
        self.time = time
        self.coordinate = coordinate
        self.normal = normal
        self.is_exiting = is_exiting
