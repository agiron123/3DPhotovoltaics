class Statistics(object):
    """This class holds information that the user will be interested in retrieving after the simulation
        has finished running. The information is held in key, value pairs in the classes info dictionary
        and an update method exists for updating the stats as needed. The update method is passed using a function
        as a first class object at the time of instantiation"""

    def __init__(self, info, update):
        """Initialize the statistics object with the given dictionary and update function."""
        self.info = info
        Statistics.update = update
        self.data = {'total_absorbed': 0, 'total_trapped': 0, 'avg_number_reflections': 0,
                     'avg_number_interactions': 0, 'avg_azimuth': 0, 'avg_zenith': 0,
                     'avg_wavelength': 0, 'number_photons': 0, 'total_number_reflections': 0,
                     'total_number_interactions': 0}
        self.total_wavelength = 0
        self.total_azimuth = 0
        self.total_zenith = 0
        self.stat_list = []

    def update(self, stat):
        if stat is not None:

            self.stat_list.append(self, stat)

            self.data['number_photons'] += 1

            if stat.absorbed:
                self.data['total_absorbed'] += 1

            if stat.trapped:
                self.data['total_trapped'] += 1

            self.data['total_number_reflections'] += stat.reflections

            self.data['total_number_interactions'] += stat.interactions

            self.data['avg_number_reflections'] = self.data['total_number_reflections']/self.data['number_photons']

            self.data['avg_number_interactions'] = self.data['total_number_interactions']/self.data['number_photons']

            self.total_wavelength += stat.wavelength
            self.data['avg_wavelength'] = self.total_wavelength / self.data['number_photons']

            self.total_azimuth += stat.azimuth
            self.data['avg_azimuth'] = self.total_azimuth / self.data['number_photons']

            self.total_zenith += stat.zenith
            self.data['avg_zenith'] = self.total_zenith / self.data['number_photons']





