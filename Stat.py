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
        #TODO: resolve this photon does not have these fields anymore, commented out for testing
        """
        self.azimuth = photon.azimuth
        self.zenith = photon.zenith"""
        self.wavelength = photon.wavelength

        """This dictionary keeps track of all of the attributes above. It will be used when outputting data
        Each attribute above should be added to the update_dictionary method below"""
        self.attributes_dictionary = {}

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

    #TODO: Determine why we are storing two copies of everything? If you  want a dictionary use the __dict__
    def update_dictionary(self):
        self.attributes_dictionary['absorbed'] = self.absorbed
        self.attributes_dictionary['trapped'] = self.trapped
        self.attributes_dictionary['path'] = self.path
        self.attributes_dictionary['reflections'] = self.reflections
        self.attributes_dictionary['interactions'] = self.interactions
        self.attributes_dictionary['azimuth'] = self.azimuth
        self.attributes_dictionary['zenith'] = self.zenith
        self.attributes_dictionary['wavelength'] = self.wavelength
        return self.attributes_dictionary