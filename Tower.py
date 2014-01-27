import Record

class Tower(object):
    """Represents a tower in the simulation. Only one tower will be modeled"""

    def __init___(self, height, material, pitch, width):
        """Initialize a tower with the given parameters"""
        self.walls = []
        #TODO : Construct walls based on height, pitch, width, and material


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
        if record is None:
            return None
        else:
            return record

