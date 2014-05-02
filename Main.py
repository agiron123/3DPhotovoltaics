"""Contains the main method which does some basic setup and conclusion steps"""
import Simulation.Simulation as Simulation
from XML_Input.GraphSettings import *
from Data_Output.Statistics import *
from Data_Output.Analysis import  *
from XML_Input.SimulationSettings import *
from XML_Input import XML_Reader
import xml.etree.ElementTree as ET


def main():
    """
    Main method for running the entire program. Will prompt the user for input and then run the simulation.
    First checks tha valid XML files for both the user input and validation file are present.
    Each simulation tag is then checked against the validation file to make sure that it is properly formatted
    and all needed information is present. If any simulation tag contains errors the user is notified of
    these errors, and the simulation is not run.
    """
    print ("Welcome to the 3D Photovoltaics Modeling.")
    done = False
    while not done:
        done = True
        filename = raw_input("Please enter the file path for your XML configuration file: ")
        try:
            valid = list(ET.parse("XML_Input/validation.xml")._root)[0]
        except Exception as e:
            done = False
            print("Validation file was not found. Validation file must be present inside of the XML_Input directory and should be named"
                  "validation.xml.")
        try:
            inputted = ET.parse(filename)
        except Exception as e:
            done = False
            print("Error opening the input file: " + e.message)
            print("Please check your file path and make sure the XML is valid")
    simulation_tags = inputted.findall("simulation")
    simulation_dicts = []
    passed_validation = True
    for i in range(len(simulation_tags)):
        errors = []
        result = XML_Reader.map_validate_xml(simulation_tags[i], valid, errors)
        if len(errors) > 0:
            passed_validation = False
            print("On simulation tag number " + str(i+1) + " there were the following errors: \n")
            for error in errors:
                print(error)
            print("\n")
        else:
            simulation_dicts.append(result)
    if passed_validation:
        #run all of the simulations here
        setting_objects = []
        for d in simulation_dicts:
            setting_objects.append((SimulationSettings(d), GraphSettings(d)))
        i = 1
        for setting in setting_objects:
            s = Statistics()
            print("Running Simulation #" + str(i))
            Simulation.run(setting[0], s)
            a = Analysis()
            a.generate_output(s, setting[0])
            a.generate_graphs(setting[1])
            i += 1

#if the user is calling this script from the command line call the main method
if  __name__ =='__main__':
    ET.parse("XML_Input/validation.xml")
    main()