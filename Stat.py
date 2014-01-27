class Stat(object):
    """Stores information that will be based to the Statistics class. Each photon has a stat.
         Stat stores all the information that could be used to compute meaningful
        statistics at a later time"""
    def __init__(self, photon):
        """Initialize the Stat information to the defaults. Information will later be updated as
        a photon moves through the simulation"""
        self.absorbed = False
        self.trapped = False
        self.path = []
        self.reflections = 0
        self.interactions = 0
        self.azimuth = photon.azimuth
        self.zenith = photon.zenith
        self.wavelength = photon.wavelength

    def absorb(self, photon, record):
        self.interactions += 1
        self.absorbed = True
        self.add_to_path(photon, record)

    def trap(self, photon, record):
        self.interactions += 1
        self.trapped = True
        self.add_to_path(photon, record)

    def reflect(self, photon, record):
        self.reflections += 1
        self.interactions += 1
        self.add_to_path(photon, record)

    def wrap_around(self, photon, record):
        self.add_to_path(photon, record)

    def exit(self, photon):
        #TODO : Implement me so that I properly calculate the exiting of a photon
        #self.add_to_path(photon, )
        return

    def add_to_path(self, photon, record):
        self.path.append((photon.position, record.coordinate))