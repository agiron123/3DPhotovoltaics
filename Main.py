import Simulation
import Statistics
import Analysis

def Main():
    """Main method for running the entire program"""
    arguments=parse_file()
    statistics=Statistics()
    Simulation.run(arguments,statistics)
    analysis=Analysis()
    analysis.generate_graphs()
    analysis.generate_output()

    #simulation is done running, now we can out the put results and perform some analysis

def parse_file(filename):
    """Parse the XML file containing the users input specifications into a dictionary"""
    return dict()

Main()