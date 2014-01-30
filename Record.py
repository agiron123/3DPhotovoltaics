class Record(object):
    """Record is used to store information relevant to photon collisions within the simulation"""

    def __init__(self, material, time, coordinate, normal):
        """Create a Record with the given parameters"""
        #this is good, avoid using null as a flag and use this boolean field instead
        self.is_boundary = (material is None)
        if not self.is_boundary:
            self.material = material
        self.time = time
        self.coordinate = coordinate
        self.normal = normal
