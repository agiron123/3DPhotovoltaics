class Record(object):
    """Record is used to store information relevant to photon collisions within the simulation"""

    def __init__(self,material,time,coordinate,normal):
        """Create a Record with the given parameters"""
        self.material=material
        self.time=time
        self.coordinate=coordinate
        self.normal=normal
