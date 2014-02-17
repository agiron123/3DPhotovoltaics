#import Simulation
#import Statistics
#import Analysis
from OutputSettings import *
from GraphSettings import *
from XMLInputParser import *

def Main():
    """Main method for running the entire program"""
    print "Welcome to 3D Photovoltaics Modeling!"
    filename = raw_input("Please enter the name of an xml file: ")
    print("Parsing ", filename)
    parser = XMLInputParser()

    arguments = parser.parse_file(filename)

    print(arguments)

    for i in range(0, len(arguments)):
        output_settings = OutputSettings(arguments[i]["OutputSettings"])
        graph_settings = GraphSettings(arguments[i]["OutputSettings"]["GraphSettings"])
    #statistics = Statistics()
    #Simulation.run(arguments, statistics)

    #simulation is done running, now we can out the put results and perform some analysis
    #analysis = Analysis()
    #analysis.generate_graphs()
    #analysis.generate_output()

Main()