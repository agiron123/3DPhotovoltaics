"""Contains the stats class"""
class Stat(object):
    """
    Stores information that will be based to the Statistics class. Each photon has a stat.
    Stat stores all the information that could be used to compute meaningful
    statistics at a later time
    """

    def __init__(self, photon):
        """
        Initialize the Stat information to the defaults. Information will later be updated as
        a photon moves through the simulation
        """
        self.absorbed = False
        self.trapped = False
        self.path = []
        self.reflections = 0
        self.interactions = 0
        self.azimuth = photon.azimuth
        self.zenith = photon.zenith
        self.wavelength = photon.wavelength

    def absorb(self, photon, record):
        """
        @type photon: A Photon object
        @param photon: The Photon to update. Updates its path
        @type record: A Record object
        @param record: The Record to update. Updates its record and path

        Increments the number of interactions and sets absorbed to true. Then adds the latest coordinate to the photon's
        path.
        """
        self.interactions += 1
        self.absorbed = True
        self.add_to_path(photon, record)

    def trap(self, photon, record):
        """
        @type photon: A Photon object
        @param photon: The Photon to update. Updates its path
        @type record: A Record object
        @param record: The Record to update. Updates its record and path

        Increments the number of interactions and sets trapped to true. Then adds the latest coordinate to the photon's
        path.
        """
        self.interactions += 1
        self.trapped = True
        self.add_to_path(photon, record)

    def reflect(self, photon, record):
        """
        @type photon: A Photon object
        @param photon: The Photon to update. Updates its path
        @type record: A Record object
        @param record: The Record to update. Updates its record and path

        Increments the number of reflections and interactions. Then adds the latest coordinate to the photon's path.
        """
        self.reflections += 1
        self.interactions += 1
        self.add_to_path(photon, record)

    def wrap_around(self, photon, record):
        """
        @type photon: A Photon object
        @param photon: The Photon to update. Updates its path
        @type record: A Record object
        @param record: The Record to update. Updates its record and path

        Adds the latest coordinate to the photon's path.
        """
        self.add_to_path(photon, record)

    def exit(self, photon):
        """
        @type photon: A Photon object
        @param photon: The Photon to update. Updates its path

        This has not been implemented yet, since it is not used by any of the graphs. We left this function here for
        future use.
        """
        #TODO : Implement me so that I properly calculate the exiting of a photon
        #self.add_to_path(photon, )
        return

    def add_to_path(self, photon, record):
        """
        @type photon: A Photon object
        @param photon: The Photon to update. Updates its path
        @type record: A Record object
        @param record: The Record to update. Updates its record and path

        Adds the latest coordinate to the photon's path.
        """
        self.path.append((photon.position, record.coordinate))