class Stat(object):
    """Stores information that will be based to the Statistics class. Each photon has a stat.
         Stat stores all the information that could be used to compute meaningful
        statistics at a later time"""
    def __init__(self):
        """Initialize the Stat information to the defaults. Information will later be updated as
        a photon moves through the simulation"""
        self.absorbed=False
        self.collisions=[]