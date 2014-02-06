import Simulation
import Statistics
import Analysis
import OutputSettings
import GraphSettings
import xml.dom.minidom
from xml.dom.minidom import parseString

def Main():
    """Main method for running the entire program"""
    arguments = parse_file("test_input.xml")
    output_settings = OutputSettings(arguments["OutputSettings"])
    graph_settings = GraphSettings(arguments["OutputSettings"]["GraphSettings"])
    statistics = Statistics()
    Simulation.run(arguments, statistics)
    analysis = Analysis()
    analysis.generate_graphs()
    analysis.generate_output()

    #simulation is done running, now we can out the put results and perform some analysis

def parse_file(filename):
    """Parse the XML file containing the users input specifications into a dictionary"""
    """Make sure that the user entered a valid xml file"""

    #open the xml file for reading:
    file = open(filename,'r')
    #convert to string:
    data = file.read()
    #close file because we dont need it anymore:
    file.close()
    #parse the xml you got from the file
    dom = parseString(data)

    #Put list of parent tags into a dictionary, to be updated after we parse the xml document
    tokens = {"Simulation" : 0, "Material_Profile" : 0, "Orbital_Properties" : 0, "Tower" : 0, "Specular_Reflection" : 0,
    "Optical_Material" : 0 , "OutputSettings" : 0}

    simulations = dom.getElementsByTagName("Simulation")
    print "Simulations Elements: \n"
    print simulations
    band_gap = dom.getElementsByTagName("band_gap")
    absorption_coefficient = dom.getElementsByTagName("absorption_coefficient")
    material_profile = {"band_gap" : handleTok(band_gap), "absorption_coefficient" : handleTok(absorption_coefficient)}
    tokens["Material_Profile"] = material_profile
    tower_shape = dom.getElementsByTagName("shape")
    pitch = dom.getElementsByTagName("pitch")
    width = dom.getElementsByTagName("width")
    height = dom.getElementsByTagName("height")
    tower = {"shape" : handleTok(tower_shape), "pitch" : handleTok(pitch), "width" : handleTok(width), "height" : handleTok(height)}
    tokens["Tower"] = tower
    specular_reflection = dom.getElementsByTagName("Specular_Reflection")
    tokens["Specular_Reflection"] = handleTok(specular_reflection)
    optical_material = dom.getElementsByTagName("Optical_Material")
    tokens["Optical_Material"] = handleTok(optical_material)
    TLE = dom.getElementsByTagName("TLE")[0]
    line_1 = TLE.getElementsByTagName("line1")[0]
    line_number1 = line_1.getElementsByTagName("line_number1")
    satellite_number = line_1.getElementsByTagName("satellite_number")
    classification = line_1.getElementsByTagName("classification")
    epoch_year = line_1.getElementsByTagName("epoch_year")
    epoch = line_1.getElementsByTagName("epoch")
    first_time_derivative = line_1.getElementsByTagName("first_time_derivative")
    second_time_derivative = line_1.getElementsByTagName("second_time_derviative")
    bstar_drag = line_1.getElementsByTagName("bstar_drag")
    ephemeris_type = line_1.getElementsByTagName("ephemeris_type")
    element_set = line_1.getElementsByTagName("element_set")
    checksum = line_1.getElementsByTagName("checksum")
    line1_dict = {"line_number" : handleTok(line_number1), "satellite_number" : handleTok(satellite_number), "classification" : handleTok(classification)}
    line_2 = TLE.getElementsByTagName("line2")[0]
    line_number2 = line_2.getElementsByTagName("line_number2")
    satellite_number2 = line_2.getElementsByTagName("satellite_number")
    inclination = line_2.getElementsByTagName("inclination")
    right_ascension = line_2.getElementsByTagName("right_ascension")
    argument_of_pedigree = line_2.getElementsByTagName("argument_of_pedigree")
    mean_anomaly = line_2.getElementsByTagName("mean_anomaly")
    mean_motion  = line_2.getElementsByTagName("mean_motion")
    revolution_number = line_2.getElementsByTagName("revolution_number")
    checksum = line_2.getElementsByTagName("checksum")
    line2_dict = {"line_number" : handleTok(line_number2), "satellite_number" : handleTok(satellite_number2), "inclination" : handleTok(inclination), "right_ascension" : handleTok(right_ascension), "argument_of_pedigree" : handleTok(argument_of_pedigree), "mean_anomaly" : handleTok(mean_anomaly), "mean_motion" : handleTok(mean_motion), "revolution_number" : handleTok(revolution_number), "checksum" : handleTok(checksum)}
    TLE_dict = {"line_1" : line1_dict, "line_2" : line2_dict}
    beta_angle = dom.getElementsByTagName("beta_angle")
    num_orbits = dom.getElementsByTagName("num_orbits")
    panel_orientation = dom.getElementsByTagName("panel_orientation")
    earthshine = dom.getElementsByTagName("earthshine")
    TLE_dict["beta_angle"] = handleTok(beta_angle)
    TLE_dict["num_orbits"] = handleTok(num_orbits)
    TLE_dict["panel_orientation"] = handleTok(panel_orientation)
    TLE_dict["earthshine"] = handleTok(earthshine)
    tokens["Orbital_Properties"] = TLE_dict
    specular_reflection = dom.getElementsByTagName("Specular_Reflection")
    optical_material = dom.getElementsByTagName("Optical_Material")
    tokens["Specular_Reflection"] = handleTok(specular_reflection)
    tokens["Optical_Material"] = handleTok(optical_material)

    #Parse out the output settings
    output_settings = dom.getElementsByTagName("OutputSettings")[0]
    powergenratio3D = output_settings.getElementsByTagName("powergenratio3D")
    max_point_power = output_settings.getElementsByTagName("maximum_point_power")
    absorption_efficiency = output_settings.getElementsByTagName("absorption_efficiency")
    absorbance = output_settings.getElementsByTagName("absorbance")
    average_interactions = output_settings.getElementsByTagName("average_interactions")
    average_reflections = output_settings.getElementsByTagName("average_reflections")
    integrated_area_ratio = output_settings.getElementsByTagName("integrated_area_ratio")
    aspect_ratio = output_settings.getElementsByTagName("aspect_ratio")
    tower_spacing_log = output_settings.getElementsByTagName("tower_spacing_log")
    tower_height = output_settings.getElementsByTagName("tower_height")
    tower_spacing = output_settings.getElementsByTagName("tower_spacing")
    azumithal_angle = output_settings.getElementsByTagName("azumithal_angle")

    #store the output settings into a dict
    output_settingsDict = {"powergenRatio3D" : handleTok(powergenratio3D), "max_point_power" : handleTok(max_point_power), "absorption_efficiency" : handleTok(absorption_efficiency), "absorbance" : handleTok(absorbance), "average_interactions" : handleTok(average_interactions), "average_reflections" : handleTok(average_reflections), "integrated_area_ratio" : handleTok(integrated_area_ratio), "aspect_ratio" : handleTok(aspect_ratio), "tower_spacing_log" : handleTok(tower_spacing_log), "tower_height" : handleTok(tower_height), "tower_spacing" : handleTok(tower_spacing), "azumithal_angle" : handleTok(azumithal_angle)}

    #parse out the graph settings
    graph_settings = dom.getElementsByTagName("GraphSettings")[0]
    max_point_powervs_zenith_angle = graph_settings.getElementsByTagName("MaxPointPowerVsZenithAngle")
    avg_reflections_vs_zenith = graph_settings.getElementsByTagName("AverageReflectionsVsAzumithal")
    absorption_efficiency_vs_azumithal = graph_settings.getElementsByTagName("AbsorptionEfficiencyVsAzumithal")
    aspect_ratio_vs_avg_reflections = graph_settings.getElementsByTagName("AspectRatioVsAverageReflections")
    integrated_aspect_ratio_vs_avgnumreflections = graph_settings.getElementsByTagName("IntegratedAreaRatioVsAvgNumReflections")
    power_ratio_3d_vs_absorbance = graph_settings.getElementsByTagName("PowerRatio3DVsAbsorbance")
    #store the graph settings into a dict
    graph_settingsDict = {"MaxPointPowerVsZenithAngle" : handleTok(max_point_powervs_zenith_angle), "AverageReflectionsVsAzumithal" : handleTok(avg_reflections_vs_zenith), "AbsorptionEfficiencyVsAzumithal" : handleTok(absorption_efficiency_vs_azumithal), "AspectRatioVsAverageReflections" :  handleTok(aspect_ratio_vs_avg_reflections), "IntegratedAreaRatioVsAvgNumReflections" : handleTok(integrated_aspect_ratio_vs_avgnumreflections), "PowerRatio3DVsAbsorbance" : handleTok(power_ratio_3d_vs_absorbance)}

    #store graph settings into the output_settings Dict
    output_settingsDict["GraphSettings"] = graph_settingsDict
    #store output_settingsDict into the tokens dict
    tokens["OutputSettings"] = output_settingsDict
    return tokens

#Helper methods for the xml parsing

def getText(nodelist):
    rc = []
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc.append(node.data)
    return ''.join(rc)

def handleTok(tokenlist):
    texts = ""
    for token in tokenlist:
        texts += " "+ getText(token.childNodes)
    return texts

Main()