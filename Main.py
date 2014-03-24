#import Simulation
#import Statistics
#import Analysis
from XML_Input.XMLInputParser import *


def main():
    """Main method for running the entire program. Will prompt the user for input and then run the simulation"""
    print ("Welcome to 3D Photovoltaics Modeling!")
    filename = raw_input("Please enter the name of an xml file: ")
    print("Parsing ", filename)
    parser = XMLInputParser()

    arguments = parser.parse_file(filename)

    print(arguments)

""" Uncomment when done debugging this part
    print "FINDING OUT WHAT'S IN ARG[I] \n"

    for i in range(0, len(arguments)):
        print arguments[i]
        output_settings = OutputSettings(arguments[i]["OutputSettings"])
        graph_settings = GraphSettings(arguments[i]["OutputSettings"]["GraphSettings"])

    print "NO LONGER FINDING OUT WHAT'S IN ARGUMENTS[I]\n"
"""

    #statistics = Statistics()
    #Simulation.run(arguments, statistics)

    #simulation is done running, now we can out the put results and perform some analysis
    #analysis = Analysis()
    #analysis.generate_graphs()
    #analysis.generate_output()

#if the user is calling this script from the command line
if  __name__ =='__main__':
    main()