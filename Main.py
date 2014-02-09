import Simulation
import Statistics
import Analysis
import OutputSettings
import GraphSettings
import XMLInputParser
import xml.dom.minidom
from xml.dom.minidom import parseString

def Main():
    """Main method for running the entire program"""
    parser = XMLInputParser("test_input.xml")
    arguments = parser.parse_file()
    output_settings = OutputSettings(arguments["OutputSettings"])
    graph_settings = GraphSettings(arguments["OutputSettings"]["GraphSettings"])
    statistics = Statistics()
    Simulation.run(arguments, statistics)
    analysis = Analysis()
    analysis.generate_graphs()
    analysis.generate_output()

    #simulation is done running, now we can out the put results and perform some analysis
Main()