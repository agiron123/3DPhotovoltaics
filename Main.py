#import Simulation
#import Statistics
#import Analysis
#from OutputSettings import *
#from GraphSettings import *
from XMLInputParser import *

def Main():
    """Main method for running the entire program"""
    parser = XMLInputParser()
    arguments = parser.parse_file("test_input.xml")
    print arguments
    #OutputSettings(arguments["OutputSettings"])
    #graph_settings = GraphSettings(arguments["OutputSettings"]["GraphSettings"])
    #statistics = Statistics()
    #Simulation.run(arguments, statistics)

    #simulation is done running, now we can out the put results and perform some analysis
    #analysis = Analysis()
    #analysis.generate_graphs()
    #analysis.generate_output()

Main()