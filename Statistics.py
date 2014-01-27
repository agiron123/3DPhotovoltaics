class Statistics(object):
    """This class holds information that the user will be interested in retrieving after the simulation
        has finished running. The information is held in key, value pairs in the classes info dictionary
        and an update method exists for updating the stats as needed. The update method is passed using a function
        as a first class object at the time of instantiation"""

    def __init__(self, info, update):
        """Initialize the statistics object with the given dictionary and update function."""
        self.info = info
        Statistics.update = update