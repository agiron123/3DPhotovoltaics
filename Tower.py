class Tower(object):
    """Represents a tower in the simulation. Only one tower will be modeled"""

    def __init___(self,walls,height,material,pitch,width):
        """Initialize a tower with the given parameters"""
        self.walls=walls
        self.height=height
        self.material=material
        self.pitch=pitch
        self.width=width

    def get_record(self,photon):
        """Given a photon return the Record corresponding to the first collision"""
        #make the records
        #sort based on time
        #return
