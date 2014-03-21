from Data_Output.Analysis import *
from XML_Input.GraphSettings import *


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

    settings_dict = {"MaxPointPowerVsZenithAngle":"False","AverageReflectionsVsAzumithal":"False",
                     "AbsorptionEfficiencyVsAzumithal":"False", "AspectRatioVsAverageReflections":"False",
                     "IntegratedAreaRatioVsAvgNumReflections":"False", "PowerRatio3DVsAbsorbance":"False",
                     "AvgInteractionsVsTowerSpacingLog":"False","AvgReflectionsVsTowerHeight":"False"}

    graph_settings = GraphSettings(settings_dict)
    analysis = Analysis()

    """
    print("making photon\n")
    azimuth = random.randint(1, 30) + 0.0
    zenith = random.randint(1, 40) + 0.0
    wavelength = random.randint(1, 50) + 0.0
    photon = Photon.Photon(np.array([0, -1, 0]), np.array([1, 1, 0]),wavelength,azimuth,zenith)
    print("made photon\n")

    print("making stats\n")
    stat_list = []
    for i in range(100):

        stat = Stat(photon)
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
        sim_sets_list.append(sim_settings)
    """
    print("outputting data\n")
    #analysis.generate_output(statistic, sim_settings)
    #analysis.generate_output(statistics_list,sim_sets_list,True)
    #analysis.save_photon_path(statistic)
    print("outputted data\n")

    print("creating graphs\n")
    analysis.generate_graphs(graph_settings)
    print("created graphs\n")

    #print("reading files\n")
    #analysis.read_files("Raw Data", "avg_azimuth", "avg_number_reflections")
    #print("read files\n")


    #print(vars(graph_settings))

Main()