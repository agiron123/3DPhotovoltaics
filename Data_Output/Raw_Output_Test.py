"""Contains some methods for testing data output functionality"""
from Data_Output.Analysis import *
from Data_Output.Statistics import *
from Data_Output.Stat import *
from XML_Input.GraphSettings import *
from XML_Input.SimulationSettings import *
import random
import numpy as np
from Simulation import Photon
import Simulation.Simulation as Simulation
from XML_Input import XML_Reader
import xml.etree.ElementTree as ET


"""This class just test if a Raw data dump works correctly. It does not use all of the functions as they should be used,
    since every required function is not implemented yet. It also just uses random values"""


def Main():
    """Main method for running the entire program"""
    """
    print "Welcome to 3D Photovoltaics Modeling!"
    filename = "viral_test_input.xml"#raw_input("Please enter the name of an xml file: ")
    print("Parsing ", filename)
    parser = XMLInputParser()

    arguments = parser.parse_file(filename)

    #print(arguments)
    for i in range(0, len(arguments)):
        output_settings = OutputSettings(arguments[i]["OutputSettings"])
        graph_settings = GraphSettings(arguments[i]["OutputSettings"]["GraphSettings"])
        #print(arguments[i]["Simple_Orbital_Properties"])
        sim_settings = SimulationSettings(arguments[i])
    #print(sim_settings)
    #print(vars(sim_settings)['tower'])
    #print(vars(sim_settings)['tower']['width'])
    tower_settings = {'width': '4', 'shape': 'square', 'height': '4' , 'pitch': '4'}

    print(vars(graph_settings))"""

    settings_dict = {"MaxPointPowerVsZenithAngle":False,"AverageReflectionsVsAzumithal":False,
                     "AbsorptionEfficiencyVsAzumithal":False, "AspectRatioVsAverageReflections":False,
                     "IntegratedAreaRatioVsAvgNumReflections":False, "PowerRatio3DVsAbsorbance":False,
                     "AvgInteractionsVsTowerSpacingLog":False,"AvgReflectionsVsTowerHeight":True}

    settings_list = ["AbsorptionEfficiencyVsAzumithal","AvgReflectionsVsTowerHeight","AverageReflectionsVsAzumithal",
                     "AvgInteractionsVsTowerSpacingLog"]

    graph_dict = {'graph_settings': settings_list}
    out_dict = {'output_settings': graph_dict}

    graph_settings = GraphSettings(out_dict)
    print(vars(graph_settings))
    analysis = Analysis()


    print("making photon\n")
    photon_list = []
    for j in range(10):
        azimuth = random.randint(1, 30) + 0.0
        zenith = random.randint(1, 40) + 0.0
        wavelength = random.randint(1, 50) + 0.0
        photon = Photon.Photon(np.array([0, -1, 0]), np.array([1, 1, 0]),wavelength,azimuth,zenith)
        photon_list.append(photon)
    print("made photon\n")

    print("making stats\n")
    stat_list = []
    for j in range(10):
        for i in range(10):
            stat = Stat(photon_list[j])
            if random.randint(1, 10) % 2 == 0:
                stat.absorbed = False
            else:
                stat.absorbed = True
            if random.randint(1, 10) % 2 == 0:
                stat.trapped = False
            else:
                stat.trapped = True
            stat.path = [1,2,3,4]
            stat.reflections = random.randint(1, 10) + 0.0
            stat.interactions = random.randint(1, 10) + 0.0

            stat_list.append(stat)
    print("made stats\n")

    statistic = Statistics()
    statistic1 = Statistics()
    statistic2 = Statistics()

    #this must be changed later when graph output is implemented
    temp = {}
    #analysis = Analysis()#Analysis(graph_settings)

    print("updating statistic\n")
    for stats in stat_list:
        statistic.update(stats)
        statistic1.update(stats)
        statistic2.update(stats)
    print("updated statistic\n")

    statistics_list = [statistic, statistic1, statistic2]
    sim_sets_list = []
    for i in range(len(statistics_list)):
        #sim_sets_list.append(sim_settings)
        sim_sets_list.append("tower data") # this is overwritten in analysis for the time being, until the parser works

    #sim_sets="tower data"
    tower_sets_dict = {'width': 40, 'shape': 'square', 'height': 10, 'pitch': 10}
    tower_dict = {'tower': tower_sets_dict}
    print("outputting data\n")
    analysis.generate_output(statistic, tower_dict)
    #analysis.generate_output(statistics_list, sim_sets_list)
    #analysis.save_photon_path(statistic)
    print("outputted data\n")

    print("creating graphs\n")
    analysis.generate_graphs(graph_settings)
    print("created graphs\n")

    #print("reading files\n")
    #analysis.read_files("Raw Data", "avg_azimuth", "avg_number_reflections")
    #print("read files\n")


    #print(vars(graph_settings))



def main2():
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
        for setting in setting_objects:
            s = Statistics()
            Simulation.run(setting[0], s)
            a = Analysis()
            print("##################################################################")
            print(setting[0])
            print("------------------------------------------------------------------")
            print(setting[0].material_profile)
            print("------------------------------------------------------------------")
            print(vars(setting[0])["material_profile"])
            print("##################################################################")
           # a.generate_output(s, setting[0])
           # a.generate_graphs(setting[1])


    #statistics = Statistics()
    #Simulation.run(arguments, statistics)

    #simulation is done running, now we can out the put results and perform some analysis
    #analysis = Analysis()
    #analysis.generate_graphs()
    #analysis.generate_output()

#Main()

main2()