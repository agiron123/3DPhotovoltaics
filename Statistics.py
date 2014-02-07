class Statistics(object):
    """This class holds information that the user will be interested in retrieving after the simulation
        has finished running. The information is held in key, value pairs in the classes info dictionary
        and an update method exists for updating the stats as needed. The update method is passed using a function
        as a first class object at the time of instantiation"""

    def __init__(self):
        """Initialize the statistics object with the given dictionary and update function."""

        #This creates the dictionary that will store all of the aggregated data
        self.data = {'total_absorbed': 0, 'total_trapped': 0, 'avg_number_reflections': 0,
                     'avg_number_interactions': 0, 'avg_azimuth': 0, 'avg_zenith': 0,
                     'avg_wavelength': 0, 'number_photons': 0, 'total_number_reflections': 0,
                     'total_number_interactions': 0}

        #These values are stored, to calculate the average of each value
        self.total_wavelength = 0
        self.total_azimuth = 0
        self.total_zenith = 0

        #This is a list that wil store all of the stat objects from a photon
        self.stat_list = []

    #This method updates the values in statistics object
    def update(self, stat):
        if stat is not None:

            #Adds a stat object to the stat_list
            self.stat_list.append(stat)

            #increments the total number of photons
            self.data['number_photons'] += 1

            #If a photon is marked as absorbed, it increments the total number of absorbed photons
            if stat.absorbed:
                self.data['total_absorbed'] += 1

            #If a photon is marked as trapped, it increments the total number of trapped photons
            if stat.trapped:
                self.data['total_trapped'] += 1

            #Increases the total number of reflections
            self.data['total_number_reflections'] += stat.reflections

            #Increases the total number of interactions
            self.data['total_number_interactions'] += stat.interactions

            #Calculates the average number of reflections
            self.data['avg_number_reflections'] = self.data['total_number_reflections']/self.data['number_photons']

            #Calculates the average number of interactions
            self.data['avg_number_interactions'] = self.data['total_number_interactions']/self.data['number_photons']

            #Increases the wavelength total and then calculates the average wavelength
            self.total_wavelength += stat.wavelength
            self.data['avg_wavelength'] = self.total_wavelength / self.data['number_photons']

            #Increases the azimuth total and then calculates the average azimuth
            self.total_azimuth += stat.azimuth
            self.data['avg_azimuth'] = self.total_azimuth / self.data['number_photons']

            #Increases the zenith total and then calculates the average zenith
            self.total_zenith += stat.zenith
            self.data['avg_zenith'] = self.total_zenith / self.data['number_photons']










