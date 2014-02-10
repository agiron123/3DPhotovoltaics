from xml.etree import ElementTree

class XMLInputParser(object):
    def __int__(self, filename):
        self.fileName = filename

        #self.validationDict = {"Simulation" : 0, "Material_Profile" : 0, "band_gap":0, "absorption_coefficient":0, "Orbital_Properties" : 0, "Tower" : 0, "shape":0, "pitch" : 0, "width" : 0, "height" : 0,"TLE" : 0, "line1" : 0, "line_number1" : 0, "satellite_number" : 0, "classification" : 0,"international_designator" : 0, "epoch_year" : 0, "epoch" : 0, "first_time_derivative" : 0, "second_time_derivative" : 0, "bstar_drag" : 0, "ephemeris_type" : 0, "element_set" : 0, "checksum" : 0, "line2" : 0, "line_number2" : 0, "satellite_number" : 0, "inclination" : 0, "right_ascension" : 0, "argument_of_pedigree" : 0, "mean_anomaly" : 0, "mean_motion" : 0, "revolution_number" : 0, "beta_angle" : 0, "num_orbits" : 0, "panel_orientation" : 0, "earthshine" : 0, "Specular_Reflection" : 0, "powergenratio3D" : 0, "maximum_point_power" : 0, "absorption_efficiency" : 0, "absorbance" : 0, "average_interactions" : 0, "average_reflections" : 0, "integrated_area_ratio" : 0, "aspect_ratio" : 0, "tower_spacing_log" : 0, "tower_height" : 0, "azumithal_angle" : 0, "GraphSettings" : 0, "MaxPointPowerVsZenithAngle" : 0, "AverageReflectionsVsAzumithal" : 0, "AbsorptionEfficiencyVsAzumithal" : 0, "AspectRatioVsAverageReflections" : 0, "IntegratedAreaRatioVsAvgNumReflections" : 0, "PowerRatio3DVsAbsorbance" : 0, "AvgInteractionsVsTowerSpacingLog" : 0, "AvgReflectionsVsTowerHeight" : 0, "Optical_Material" : 0, "OutputSettings" : 0}
        #Need to make sure that we are distinguishing between parameters that appear twice like checksum.
        #Keep incrementing that parameter, no need to have it twice in the dictionary.

    def parse_file(self, file):
        """Parse the XML file containing the users input specifications into a dictionary"""
        """Make sure that the user entered a valid xml file"""
        #TODO: Move this back up. Was being a pain for some reason
        validationDict = {"Simulation" : 0, "Material_Profile" : 0,
                               "band_gap":0, "absorption_coefficient":0,
                               "Orbital_Properties" : 0, "Tower" : 0, "shape":0, "pitch" : 0, "width" : 0, "height" : 0,
                               "TLE" : 0, "line1" : 0, "line_number1" : 0, "satellite_number" : 0, "classification" : 0,
                               "international_designator" : 0, "epoch_year" : 0, "epoch" : 0, "first_time_derivative" : 0,
                               "second_time_derivative" : 0, "bstar_drag" : 0, "ephemeris_type" : 0, "element_set" : 0,
                               "checksum" : 0, "line2" : 0, "line_number2" : 0, "satellite_number" : 0, "inclination" : 0,
                               "right_ascension" : 0, "argument_of_pedigree" : 0, "mean_anomaly" : 0, "mean_motion" : 0,
                               "revolution_number" : 0, "beta_angle" : 0, "num_orbits" : 0, "panel_orientation" : 0, "earthshine" : 0,
                               "Specular_Reflection" : 0, "powergenratio3D" : 0, "maximum_point_power" : 0, "absorption_efficiency" : 0,
                               "absorbance" : 0, "average_interactions" : 0, "average_reflections" : 0, "integrated_area_ratio" : 0,
                               "aspect_ratio" : 0, "tower_spacing_log" : 0, "tower_height" : 0, "azumithal_angle" : 0, "GraphSettings" : 0,
                               "MaxPointPowerVsZenithAngle" : 0, "AverageReflectionsVsAzumithal" : 0, "AbsorptionEfficiencyVsAzumithal" : 0,
                               "AspectRatioVsAverageReflections" : 0, "IntegratedAreaRatioVsAvgNumReflections" : 0, "PowerRatio3DVsAbsorbance" : 0,
                               "AvgInteractionsVsTowerSpacingLog" : 0, "AvgReflectionsVsTowerHeight" : 0, "Optical_Material" : 0, "OutputSettings" : 0}
                                #Need to make sure that we are distinguishing between parameters that appear twice like checksum.
                                #Keep incrementing that parameter, no need to have it twice in the dictionary.

        tokens = {}
        with open(file, 'rt') as f:
            tree = ElementTree.parse(f)

        for node in tree.getiterator():
            tokens[node.tag] = node.text
            validationDict[node.tag] = validationDict.get(node.tag, 0) + 1

        print "Finished parsing the file. \n Validation Dictionary: \n"
        #print self.validationDict
        print "Tokens: \n"

        #Check each of the values in the validation dictionary, add them to list if the parameter has a value of 0
        list = []
        for k, v in validationDict.iteritems():
            print "Key : " + k
            print "Value: "
            print v
            if v == 0:
                list.append(k)

        print "Parameters that need to be re entered: \n"
        print list
        return tokens




