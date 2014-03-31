class Statistics(object):
    """This class holds information that the user will be interested in retrieving after the simulation
        has finished running. The information is held in key, value pairs in the classes info dictionary
        and an update method exists for updating the stats as needed. The update method is passed using a function
        as a first class object at the time of instantiation"""

    def __init__(self):
        """Initialize the statistics object with the given dictionary and update function."""

        #This creates the dictionary that will store all of the aggregated data
        self.data = {'total_absorbed': 0.0, 'total_trapped': 0.0, 'avg_number_reflections': 0.0,
                     'avg_number_interactions': 0.0, 'number_photons': 0.0, 'total_number_reflections': 0.0,
                     'total_number_interactions': 0.0, 'absorption_efficiency': 0.0}

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

            #Calculates the absorption_efficiency
            self.data['absorption_efficiency'] = self.data['total_absorbed'] / self.data['number_photons']