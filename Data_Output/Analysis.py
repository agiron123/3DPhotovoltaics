import csv
import os
import matplotlib.pyplot as plt
import numpy as np
from random import *
from shutil import copy
from datetime import datetime
from re import match


class Analysis(object):
    """Used to output information from the simulation. Has access to all of the information held in
        Statistics. This information can be outputted in raw form, or analyzed further, including transformation
        into graphs and figures. Methods for generating output in various forms are passed using functions as first
        class objects at the time of instantiation """

    #--------------------------------------------------------------------
    #These variables are generic tags used through the this python file
    # they determine the name of files and headers in csv files

    #.csv Headers
    tower_data_tag = "Tower Data"
    compiled_data_tag = "Compiled Data"
    stats_data_tag = "Stats"
    material_data_tag = "Material Profile"

    #Folder names
    output_folder_tag = "Simulation_Data"
    most_recent_tag = "Most_Recent_Run"
    raw_data_folder_tag = "Raw_Data"

    #File names
    raw_data_file_tag = "Raw_Sim_Data_"

    #Units
    distance_unit_tag = " (Micrometers)"
    angle_unit_tag = " (Degrees)"
    wavelength_unit_tag = " (Nanometers)"
    percent_unit_tag = " (%)"
    abs_coeff_unit_tag = " (1/cm)"
    band_gap_unit_tag = " (Electronvolts)"

    #Solar Panel dimensions (micrometers)
    #TODO: Get actual values
    length = 0
    width = 0
    height = 0
    #---------------------------------------------------------------------

    last_simulation = ""

    def __init__(self):
        """
        Bind the functions passed in to the Analysis object
        """
        self.folder_dir = self.folder_creator(None)
        self.most_recent_dir = self.folder_creator(self.most_recent_tag)

    def save_photon_path(self, statistic):
        """
        This function creates csv files that save only a photon's path. This is only for debugging
        """
        #name of the folder and csv files
        data_file_name = 'Photon_Path_'
        data_folder_name = 'Photon Paths'
        #creates the folder and file
        self.folder_dir = self.folder_creator(data_folder_name)
        file_location = self.file_path_creator(self.folder_dir, data_file_name, ".csv")
        #attempts to open the file for reading
        try:
            file_name = open(file_location, 'wb')
        except csv.Error as e:
            print("Couldn't open the csv file. If it is opened in another program, please close it")
        else:
            #begins writing to the file
            writer = csv.writer(file_name)
            #gets the list of stats
            stat_list = statistic.stat_list
            writer.writerow(["Photon Paths"])
            #print(vars(stat_list[0]).values())
            #print(vars(stat_list[0]).values()[7])
            #for each stat it gets the path of the photon at index 7
            for stat in stat_list:
                writer.writerow(vars(stat).values()[7])
            file_name.close()

    def generate_output(self, statistics, sim_settings, save_path=False):
        """
        This method creates a .csv file with all of the data from a simulation. It takes in  a list of statistics
        and whether or not to save a photon's path, it then generates a csv file for each statistic/simulation
        """
        #The name of the .csv file
        data_file_name = self.raw_data_file_tag
        #The name of the folders for the raw data .csv files
        data_folder_name = self.raw_data_folder_tag

        #Creates the folder
        self.folder_dir = self.folder_creator(data_folder_name)

        #This empties the most_recent_dir folder so more recent files can be save there
        for files in os.listdir(self.most_recent_dir):
            path = os.path.join(self.most_recent_dir, files)
            try:
                os.remove(path)
            except WindowsError as e:
                print("NOT deleted: "+path+"\n")
                pass

        print("Creating Output .csv File\n")

        #Checks if the given stat is in a list, if not it puts it into a list
        if type(statistics) != list:
            statistics = [statistics]
        if type(sim_settings) != list:
            sim_settings = [sim_settings]

        #checks there are an equal number of statistics as there are simulation settings
        if len(statistics) != len(sim_settings):
            raise ValueError("Number of statistics doesn't match number of simulation settings. "
                             + "\nNumber of statics should be match number of simulation settings\n")

        #This for loop allows it to output data for multiple simulations
        for index in range(len(statistics)):
            #Copies the data dictionary from a statistic
            compiled_data = statistics[index].data

            #gets the tower's setting from the simulation settings
            #TODO: Uncomment following two lines if not testing or debugging this file
            tower_settings = vars(sim_settings[index])['tower']
            material_data = sim_settings[index].material_profile

            #----------------------------------------------------------------------------------------------------------
            #TODO: remove print statements and remove the overwrite of tower settings
            # This was for testing when the xml parser did not work to use this you need to comment out the line above
            #print("\n Tower settings changes\n")
            #width = randint(1, 10)*10.0
            #height = randint(1, 10)*10.0
            #pitch = randint(1, 10)*10.0
            #abs_coeff = randint(1, 10)*1000000.0
            #band_gap = randint(1, 200)/100.0
            #tower_settings = {'width': str(width), 'shape': 'square', 'height': str(height), 'pitch': str(pitch)}
            #material_data = {'absorption_coefficient': str(abs_coeff), 'band_gap': str(band_gap)}
            #print("\n End of tower settings changes\n")
            #----------------------------------------------------------------------------------------------------------

            #adds the aspect ratio and log of the tower pitch to the tower settings
            self.add_tower_info(tower_settings)
            print("\nEnd of Tower Settings Changes\n")

            #Creates the csv file and stores the location for later use
            file_location = self.file_path_creator(self.folder_dir, data_file_name, ".csv")

            #Opens a .csv file to write to or overwrites an existing file with the same name
            try:
                file_name = open(file_location, 'wb')
            except csv.Error as e:
                print("++++ERROR++++ Couldn't open the csv file. " +
                      "If it is opened in another program, please close it and run the simulation again")
            else:
                #Creates the writer object for a given file
                writer = csv.writer(file_name)

                #writes the material profile data to the .csv file
                writer.writerow([self.material_data_tag])
                #adds units to the material profile keys
                material_keys_units = self.add_units(material_data.keys())
                writer.writerow(material_keys_units)
                writer.writerow(material_data.values())

                #Writes the tower data to the .csv file
                writer.writerow([self.tower_data_tag])
                #adds units to the tower data keys
                tower_keys_units = self.add_units(tower_settings.keys())
                writer.writerow(tower_keys_units)
                writer.writerow(tower_settings.values())

                #Writes the compiled data to the .csv file
                writer.writerow([self.compiled_data_tag])
                #adds units to the compiled data keys
                compiled_keys_units = self.add_units(compiled_data.keys())
                writer.writerow(compiled_keys_units)
                writer.writerow(compiled_data.values())

                #Writes the word "Stats" to the next row of the .csv file
                writer.writerow([self.stats_data_tag])

                #Copies the stat_list from statistics
                stat_list = statistics[index].stat_list
                if len(stat_list) != 0:

                    #Gets a stat's dictionary in order to write the stat's attributes to the csv file
                    stat_dict = vars(stat_list[0])
                    if save_path is False and "path" in stat_dict:
                        del stat_dict["path"]
                    #adds units to the material profile keys
                    stat_keys_units = self.add_units(stat_dict.keys())
                    writer.writerow(stat_keys_units)
                    writer.writerow(stat_dict.values())

                    #This will print each stat's contents in the .csv file
                    for stat in stat_list[1:]:
                        stat_dict = vars(stat)
                        if save_path is False and "path" in stat_dict:
                            del stat_dict['path']
                        stat_dict = stat_dict.values()
                        writer.writerow(stat_dict)

                    #Closes the .csv file
                    file_name.close()

                    #Copies the new file to the most_recent_dir folder
                    copy(file_location, self.most_recent_dir)

                    self.last_simulation = file_location
                    print("Data has been outputted in to a .csv file\n")
                    print("The file location is: " + file_location + "\n")
                else:
                    #close and removes the files since it does not have any data
                    file_name.close()
                    os.remove(file_location)

    def folder_creator(self, folder_name):
        """
        This function creates a folder, with the name taken from folder_name, that stores all of the .csv files for the
        output function. It also creates the path to that folder and returns the path
        """
        #gets the currents scripts directory
        script_dir = os.path.dirname(os.path.abspath(__file__))
        #adds the new folder to the directory
        if folder_name is None:
            destination_dir = os.path.join(script_dir, self.output_folder_tag)
        else:
            destination_dir = os.path.join(script_dir, self.output_folder_tag, folder_name)

        #creates the new folder
        try:
            os.makedirs(destination_dir)
        except OSError:
            pass  # folder already exist
        return destination_dir


    @staticmethod
    def file_path_creator(destination_dir, file_name, extension):
        """
        This function helps create the .csv file, with the value taken from file_name. To create multiple files for
        different runs, this function uses regex to check the files in the directory to determine the number of
        the most recent run and then increments it by 1. It then returns the path to the file
        """
        # gets the timestamp and converts it to a string in with a "YYYY-MM-DD HH:MM:SS.ss" format
        time_stamp = str(datetime.now())
        # formats the timestamp to: "YYYY-MM-DD HH-MM-SS.ss" format
        time_stamp = time_stamp.replace(':', '-')
        #new_file_name = file_name + sim_number + extension
        new_file_name = file_name + time_stamp + extension
        #creates the path to the new data file
        path = os.path.join(destination_dir, new_file_name)
        return path

    def generate_graphs(self, graph_settings):
        """
        This function takes in a graph_settings object and determines which graph to make. It first creates the folder
        for each type of graph. Then it creates a path to that file location. It then calls the correct method to
        make a the .csv file used to generate the graphs. Finally it calls the function to generate the graphs.
        """
        #the directory of the raw_data
        data_dir = self.folder_dir

        #lists that store all of the file locations, axis labels, and output locations
        # so the it can update all of the graph .csv files in one call
        file_locations = []
        axis_labels = []
        output_directories = []
        #the graphs that have an angle value need to use a different function from the other graphs and thus must be
        # separated
        file_locations_angles =[]
        axis_labels_angles = []
        output_directories_angles = []

        #checks if there are multiple simulations before creating graph
        if len(os.listdir(data_dir)) >= 1:
            print("Creating graphs")
            #gets the dictionary contain which graphs to make
            settings_dict = vars(graph_settings)

            #these if statements all follow a similar format.
            # 1) first it checks if the graph should be created
            # 2) creates the folder to store the .csv file
            # 3) creates the location of the .csv file
            # 4) gets the axis labels and write the labeling data to the .csv file
            # 5) stores the information into the data lists above

            if settings_dict["MaxPointPowerVsZenithAngle"] is True:
                print("Creating Max Point Power vs Zenith Angle Graph")
                output_dir = self.folder_creator("Max_Point_Power_vs_Zenith_Angle")
                file_location = self.file_path_creator(output_dir, "Max_Point_Pwr_vs_Zenith_", ".csv")
                #TODO: finish implementing
                print("generate_graphs in Analysis.py is not fully implemented yet." +
                      "\nCannot create Max Power vs Zenith Angle graph\n")
                #self.max_power_vs_zenith(file_location)

            if settings_dict["AverageReflectionsVsAzimuthal"] is True:
                print("Creating Average Number of Reflections vs Azimuthal Angle Graph")
                output_dir = self.folder_creator("Average_Reflections_vs_Azimuth_Angle")
                file_location = self.file_path_creator(output_dir, "Avg_Reflections_vs_Azimuthal_", ".csv")
                labels = self.avg_reflections_vs_azimuthal(file_location)
                file_locations_angles.append(file_location)
                output_directories_angles.append(output_dir)
                axis_labels_angles.append(labels)

            if settings_dict["AbsorptionEfficiencyVsAzimuthal"] is True:
                print("Creating Absorption Efficiency vs Azimuthal Graph")
                output_dir = self.folder_creator("Absorption_Efficiency_vs_Azimuth_Angle")
                file_location = self.file_path_creator(output_dir, "Absorption_Efficiency_vs_Azimuthal_", ".csv")
                labels = self.absorption_efficiency_vs_azimuthal(file_location)
                file_locations_angles.append(file_location)
                output_directories_angles.append(output_dir)
                axis_labels_angles.append(labels)

            #Checks if any of the angle graphs should be created
            if len(file_locations_angles) > 0:
                #Calls the function to add the data to the .csv files
                self.add_graph_data_to_csv_angle(self.last_simulation, file_locations_angles, axis_labels_angles)
                #Creates the actual graph
                for index in range(len(output_directories_angles)):
                    self.create_graph(output_directories_angles[index], file_locations_angles[index])

            # there needs to be more than one raw_data file for these graphs
            if len(os.listdir(data_dir)) > 1:

                # again these if statement follow the same format as above.
                # 1) first it checks if the graph should be created
                # 2) creates the folder to store the .csv file
                # 3) creates the location of the .csv file
                # 4) gets the axis labels and write the labeling data to the .csv file
                # 5) stores the information into the data lists above

                if settings_dict["AspectRatioVsAverageReflections"] is True:
                    print("Creating Aspect Ratio vs Average Reflections Graph")
                    output_dir = self.folder_creator("Aspect_Ratio_vs_Average_Number_of_Reflections")
                    file_location = self.file_path_creator(output_dir, "Aspect_Ratio_vs_Avg_Reflections_", ".csv")
                    labels = self.aspect_ratio_vs_avg_reflections(file_location)
                    file_locations.append(file_location)
                    output_directories.append(output_dir)
                    axis_labels.append(labels)

                if settings_dict["IntegratedAreaRatioVsAvgNumReflections"] is True:
                    print("Creating Integrated Area Ratio vs Average Number Reflections Graph")
                    output_dir = self.folder_creator("Integrated_Area_Ratio_vs_Avg_Num_Reflections")
                    file_location = self.file_path_creator(output_dir, "Integrated_Area_Ratio_vs_Avg_Reflections_", ".csv")
                    #TODO: finish implementing
                    print("generate_graphs in Analysis.py is not fully implemented yet." +
                          "\n Cannot create Integrated Area Ratio vs Avgerage Number of Reflections graph\n")
                    #self.integrated_area_ratio_vs_avg_num_reflections(file_location)

                if settings_dict["PowerRatio3DVsAbsorbance"] is True:
                    print("Creating 3D Power Ratio vs Absorbance Graph")
                    output_dir = self.folder_creator("Power_Ratio_3D_vs_Absorbance")
                    file_location = self.file_path_creator(output_dir, "Power_Ratio_3D_vs_Absorbance_", ".csv")
                    #TODO: finish implementing
                    print("generate_graphs in Analysis.py is not fully implemented yet. " +
                          "\n Cannot create Power Ratio vs Absorbance graph\n")
                    #self.power_ratio_vs_absorbance(file_location)

                if settings_dict["AvgInteractionsVsTowerSpacingLog"] is True:
                    print("Creating Average Number of Interactions vs Log of Tower Pitch Graph")
                    output_dir = self.folder_creator("Average_Number_of_Interactions_vs_Tower_Pitch_Log")
                    file_location = self.file_path_creator(output_dir, "Avg_Interactions_vs_Tower_Pitch_Log_", ".csv")
                    labels = self.avg_interactions_vs_tower_spacing(file_location)
                    file_locations.append(file_location)
                    output_directories.append(output_dir)
                    axis_labels.append(labels)

                if settings_dict["AvgReflectionsVsTowerHeight"] is True:
                    print("Creating Average Number of Reflections vs Tower Height Graph")
                    output_dir = self.folder_creator("Average_Number_of_Reflections_vs_Tower_Height")
                    file_location = self.file_path_creator(output_dir, "Avg_Reflections_vs_Tower_Height_", ".csv")
                    labels = self.avg_reflections_vs_tower_height(file_location)
                    file_locations.append(file_location)
                    output_directories.append(output_dir)
                    axis_labels.append(labels)

                #checks if any of the graphs should be created.
                if len(file_locations) > 0:
                    #Calls the function to add the data to the .csv files
                    self.add_graph_data_to_csv(self.folder_dir, file_locations, axis_labels)
                    #Creates the actual graphs
                    for index in range(len(output_directories)):
                        self.create_graph(output_directories[index], file_locations[index])

            else:
                print("Need to run more than one simulation for the following graphs:\n" +
                      "Aspect Ratio vs Average Reflections\n" +
                      "Integrated Area Ratio vs Average Number Reflections\n" +
                      "3D Power Ratio vs Absorbance\n" +
                      "Average Number of Interactions vs Log of Tower Pitch\n" +
                      "Average Number of Reflections vs Tower Height\n")

            print("Finished creating graphs")
        else:
            print("Need to run at least one simulation before being able to create a graph")

    # ---- These functions Create the .csv file for each type of graph -------------------------------------------------
    #TODO: check the types of desired graphs and how to graph them
    def max_power_vs_zenith(self, file_location):
        """
        This function creates the csv file for the Max Power vs Zenith Angle graph.
        It takes in the file location for the .csv file and returns the axis labels needed when creating the graph.
        Essentially it defines the title and axis labels for the graph. Then it calls the function to write them
        to the .csv file.
        """
        #TODO: finish implementing

    def avg_reflections_vs_azimuthal(self, file_location):
        """
        This function creates the csv file for the Average Number of Reflections vs Azimuthal Angle graph.
        It takes in the file location for the .csv file and returns the axis labels needed when creating the graph.
        Essentially it defines the title and axis labels for the graph. Then it calls the function to write them
        to the .csv file.
        """
        title = "Average Number of Reflections vs Azimuthal Angle"
        x_label = "Azimuthal Angle"+self.angle_unit_tag
        y_label = "Average Number of Reflections"
        self.write_graph_labels(file_location, title, x_label, y_label)
        #self.add_graph_data_to_csv_angle(self.last_simulation, file_location, "azimuth", "avg_number_reflections")
        return ("azimuth", "avg_number_reflections")

    def absorption_efficiency_vs_azimuthal(self, file_location):
        """
        This function creates the csv file for the Absorption Efficiency vs Azimuthal Angle graph.
        It takes in the file location for the .csv file and returns the axis labels needed when creating the graph.
        Essentially it defines the title and axis labels for the graph. Then it calls the function to write them
        to the .csv file.
        """
        title = "Absorption Efficiency vs Azimuthal Angle"
        x_label = "Azimuthal Angle"+self.angle_unit_tag
        y_label = "Absorption Efficiency"
        self.write_graph_labels(file_location, title, x_label, y_label)
        #self.add_graph_data_to_csv_angle(self.last_simulation, file_location, "azimuth", "absorption_efficiency")
        return ("azimuth", "absorption_efficiency")

    def aspect_ratio_vs_avg_reflections(self, file_location):
        """
        This function creates the csv file for the Aspect Ratio vs Average Number of Reflections graph.
        It takes in the file location for the .csv file and returns the axis labels needed when creating the graph.
        Essentially it defines the title and axis labels for the graph. Then it calls the function to write them
        to the .csv file.
        """
        title = "Aspect Ratio vs Average Number of Reflections"
        x_label = "Aspect Ratio"+self.distance_unit_tag
        y_label = "Average Number of Reflections"
        self.write_graph_labels(file_location, title, x_label, y_label)
        #self.add_graph_data_to_csv(self.folder_dir, file_location, "aspect_ratio", "avg_number_reflections", True)
        return ("aspect_ratio", "avg_number_reflections")

    def integrated_area_ratio_vs_avg_num_reflections(self, file_location):
        """
        This function creates the csv file for the Integrated Area Ratio vs Average Number Reflections graph.
        It takes in the file location for the .csv file and returns the axis labels needed when creating the graph.
        Essentially it defines the title and axis labels for the graph. Then it calls the function to write them
        to the .csv file.
        """
        #TODO: finish implementing

    def power_ratio_vs_absorbance(self, file_location):
        """
        This function creates the csv file for the 3D Power Ratio vs Absorbance graph.
        It takes in the file location for the .csv file and returns the axis labels needed when creating the graph.
        Essentially it defines the title and axis labels for the graph. Then it calls the function to write them
        to the .csv file.
        """
        #TODO: finish implementing

    def avg_interactions_vs_tower_spacing(self, file_location):
        """
        This function creates the csv file for the Average Number of Interactions vs Tower Pitch graph.
        It takes in the file location for the .csv file and returns the axis labels needed when creating the graph.
        Essentially it defines the title and axis labels for the graph. Then it calls the function to write them
        to the .csv file.
        """
        title = "Average Number of Interactions vs Tower Pitch"
        x_label = "Tower Pitch"+self.distance_unit_tag
        y_label = "Average Number of Interactions"
        self.write_graph_labels(file_location, title, x_label, y_label)
        #self.add_graph_data_to_csv(self.folder_dir, file_location, "pitch", "avg_number_interactions", True)
        return ("pitch", "avg_number_interactions")

    def avg_reflections_vs_tower_height(self, file_location):
        """
        This function creates the csv file for the Average Number of Reflections vs Tower Height graph.
        It takes in the file location for the .csv file and returns the axis labels needed when creating the graph.
        Essentially it defines the title and axis labels for the graph. Then it calls the function to write them
        to the .csv file.
        """
        title = "Average Number of Reflections vs Tower Height"
        x_label = "Tower Height"+self.distance_unit_tag
        y_label = "Average Number of Reflections"
        self.write_graph_labels(file_location, title, x_label, y_label)
        #self.add_graph_data_to_csv(self.folder_dir, file_location, "height", "avg_number_reflections", True)
        return ("height", "avg_number_reflections")
    # ------------------------------------------------------------------------------------------------------------------

    def add_tower_info(self, tower_settings):
        """
        This function takes in the tower settings dictionary and adds the aspect ration and log of the tower pitch
        """
        tower_settings["aspect_ratio"] = float(tower_settings['width'])/float(tower_settings['height'])
        tower_settings["log_pitch"] = np.log(float(tower_settings['pitch']))

    def add_graph_data_to_csv(self, data_directory, output_file_locations=[], axis_labels=[]):
        """
        This function creates the csv file needed to create graphs with out an angle value.
        It can create the .csv files for multiples graphs in one function call.
        It takes in a list of output file locations which will be the location of a graph's .csv file. It also takes
        in the associated axis pair for each graph.
        """

        #check if the parameters are valid
        if output_file_locations != [] and len(output_file_locations) == len(axis_labels):

            #lists that store the data from all of the raw_data .csv files
            tower_keys = []
            tower_data = []
            compiled_keys = []
            compiled_data = []

            #Looks through all of the files in the given data_directory and opens the .csv files for reading
            for files in os.listdir(data_directory):
                if files.endswith(".csv") and self.raw_data_file_tag in files:
                    file_dir = os.path.join(data_directory, files)
                    try:
                        file_name = open(file_dir, 'rb')
                    except csv.Error as e:
                        print("++++ERROR++++ Couldn't open the csv file. " +
                              "If it is opened in another program, please close it and run the simulation again")
                    reader = csv.reader(file_name)

                    #gets the first line in the .csv file
                    data_type = reader.next()

                    #gets the tower data
                    if data_type[0] == self.tower_data_tag:
                        twr_key = reader.next()
                        twr_values = reader.next()
                    else:
                        while data_type[0] != self.tower_data_tag:
                            data_type = reader.next()
                        twr_key = reader.next()
                        twr_values = reader.next()

                    #removes the units from the tower keys and then appends it to the main data lists
                    twr_key = self.remove_units(twr_key)
                    tower_keys.append(twr_key)
                    tower_data.append(twr_values)

                    #Gets the Compiled Data
                    if data_type[0] == self.compiled_data_tag:
                        keys = reader.next()
                        values = reader.next()
                    else:
                        while data_type[0] != self.compiled_data_tag:
                            data_type = reader.next()
                        keys = reader.next()
                        values = reader.next()

                    #removes the units from the compiled data keys and then appends it to the main data lists
                    keys = self.remove_units(keys)
                    compiled_keys.append(keys)
                    compiled_data.append(values)

                    file_name.close()

            #Interates through the file locations to write to the graph .csv
            for index in range(len(output_file_locations)):
                #Gets the axis labels and location of the current graph
                x_value = axis_labels[index][0]
                y_value = axis_labels[index][1]
                output_file_location = output_file_locations[index]

                #opens the graph .csv file to be appended to
                try:
                    graph_file = open(output_file_location, 'ab')
                except csv.Error as e:
                    print("++++ERROR++++ Couldn't open the csv file. "
                          + "If it is opened in another program, please close it and run the simulation again")
                #creates writer object
                writer = csv.writer(graph_file)

                #interates through all of the data from the raw_data files
                for data in range(len(compiled_data)):
                    #A boolean to validate whether a key exists in the key list
                    found_values = False

                    #checks if the x_value is a tower value
                    if x_value in tower_keys[data]:
                        tower_val = True
                    else:
                        tower_val = False

                    #Gets the index of the desired y_value
                    if y_value in compiled_keys[data]:
                        y = compiled_keys[data].index(y_value)
                        found_values = True
                    else:
                        #if it didn't find the y_value then this set should be tossed out
                        found_values = False
                        print("The y value "+y_value+" is not in " + self.compiled_data_tag + "." +
                              "\nCheck if you are looking for the correct value and in the correct list")

                    #Gets the index of the desired x_value and then writes the data point to the graph .csv file
                    if tower_val is True and found_values is True:
                        if x_value in tower_keys[data]:
                            x = tower_keys[data].index(x_value)
                            found_values = True
                        else:
                            #if it didn't find the x_value then this set should be tossed out
                            found_values = False
                            print("The tower x value "+x_value+" is not in " + self.tower_data_tag + "." +
                                  "\nCheck if you are looking for the correct value and in the correct list")
                        if found_values is True:
                            #write the coordinate point to the .csv file
                            writer.writerow([float(tower_data[data][x]), float(compiled_data[data][y])])
                    else:
                        if x_value in compiled_keys[data]:
                            x = compiled_keys[data].index(x_value)
                            found_values = True
                        else:
                            #if it didn't find the x_value then this set should be tossed out
                            found_values = False
                            print("The x value "+x_value+" is not in " + self.compiled_data_tag + "." +
                                  "\nCheck if you are looking for the correct value and in the correct list")
                        if found_values is True:
                            #write the coordinate point to the .csv file
                            writer.writerow([float(compiled_data[data][x]), float(compiled_data[data][y])])

                #closes the graph .csv file and copies it to Most_Recent_Run folder.
                graph_file.close()
                copy(output_file_location, self.most_recent_dir)
        else:
            print("++++ERROR++++ Can't create graphs without all of the required information")


    def add_graph_data_to_csv_angle(self, data_file, output_file_locations=[], axis_labels=[]):
        #TODO:Fully implement this!!!!!!!!!!!!!!
        """
        This function creates the .csv file needed to create graphs with an angle value.
        It can make multiple .csv with one call and only uses the data from the LATEST simulation .csv file (data_file).
        It takes in a list of output file locations which will be the location of a graph's .csv file. It also takes
        in the associated axis pair for each graph.
        """
        #checks if the parameters are valid
        if output_file_locations != [] and len(output_file_locations) == len(axis_labels):
            #checks if data_file is valid
            if data_file.endswith(".csv") and self.raw_data_file_tag in data_file:
                try:
                    file_name = open(data_file, 'rb')
                except csv.Error as e:
                    print("++++ERROR++++ Couldn't open the csv file. " +
                          "If it is opened in another program, please close it and run the simulation again")
                #sets the reader object for the file
                reader = csv.reader(file_name)

                #gets the first line in the .csv file
                data_type = reader.next()

                #gets the tower data
                if data_type[0] == self.tower_data_tag:
                    tower_keys = reader.next()
                    tower_values = reader.next()
                else:
                    while data_type[0] != self.tower_data_tag:
                        data_type = reader.next()
                    tower_keys = reader.next()
                    tower_values = reader.next()

                #removes the units from teh tower_keys
                tower_keys = self.remove_units(tower_keys)

                #Gets the Compiled Data
                if data_type[0] == self.compiled_data_tag:
                    data_keys = reader.next()
                    data_values = reader.next()
                else:
                    while data_type[0] != self.compiled_data_tag:
                        data_type = reader.next()
                    data_keys = reader.next()
                    data_values = reader.next()

                #removes the units from the data_keys
                data_keys = self.remove_units(data_keys)

                #Dictionaries that store the data for each stat based on the x_value
                zenith_dict = {}
                azimuth_dict = {}
                wavelength_dict = {}

                #Locates the photon/stat data and gets the keys
                if data_type[0] == self.stats_data_tag:
                    stat_keys = reader.next()
                else:
                    while data_type[0] != self.stats_data_tag:
                        data_type = reader.next()
                    stat_keys = reader.next()

                stat_keys = self.remove_units(stat_keys)

                # this goes through the stat keys and gets their indices for later use
                for index in range(len(stat_keys)):
                    if stat_keys[index] == "zenith":
                        zenith_index = index
                    elif stat_keys[index] == "azimuth":
                        azimuth_index = index
                    elif stat_keys[index] == "wavelength":
                        wavelength_index = index
                    elif stat_keys[index] == "interactions":
                        interactions_index = index
                    elif stat_keys[index] == "trapped":
                        trapped_index = index
                    elif stat_keys[index] == "absorbed":
                        absorbed_index = index
                    elif stat_keys[index] == "reflections":
                        reflections_index = index

                #------------------
                # These values are the indices used when compiled the data for a given angle in the loop below
                # They should match the order that values are appended in the following if-else statement
                inter_in = 0
                trap_in = 1
                abs_in = 2
                refl_in = 3
                tot_in = 4
                #-------------------

                #this gets all of the stat data
                for row in reader:
                    #this is a list to store the data from a stat at a given angle
                    stat_vals = []

                    #it first checks if the angle is already in the dictionary
                    if row[azimuth_index] in azimuth_dict:
                        #sets the stat_vals list to the already existing list
                        stat_vals = azimuth_dict[row[azimuth_index]]
                        #updates stat_vals values
                        stat_vals[inter_in] += float(row[interactions_index])
                        if row[trapped_index] == "True":
                            stat_vals[trap_in] += 1.0
                        if row[absorbed_index] == "True":
                            stat_vals[abs_in] += 1.0
                        stat_vals[refl_in] += float(row[reflections_index])
                        stat_vals[tot_in] += 1.0
                    else:
                        #if the angle isn't in the dictionary then it creates a new stat_vals list for the angle

                        #number of interacitons
                        stat_vals.append(float(row[interactions_index]))
                        #trapped photon count
                        if row[trapped_index] == "True":
                            stat_vals.append(1.0)
                        else:
                            stat_vals.append(0.0)
                        #absorbed photon count
                        if row[absorbed_index] == "True":
                            stat_vals.append(1.0)
                        else:
                            stat_vals.append(0.0)
                        #number of reflections
                        stat_vals.append(float(row[reflections_index]))
                        #total number of photons at the given angle
                        stat_vals.append(1.0)
                        #adds the stat_val list to the dictionary. The key being the associated angle
                        azimuth_dict[row[azimuth_index]] = stat_vals
                file_name.close()

                #this part write to the .csv file based on the graph it has to make
                for index in range(len(output_file_locations)):
                    #gets the axis labels and .csv file for the current graph
                    x_value = axis_labels[index][0]
                    y_value = axis_labels[index][1]
                    output_file_location = output_file_locations[index]

                    #opens the graph .csv file to be append to
                    try:
                        graph_file = open(output_file_location, 'ab')
                    except csv.Error as e:
                        print("++++ERROR++++ Couldn't open the csv file. " +
                              "If it is opened in another program, please close it and run the simulation again")
                    #creates writer object
                    writer = csv.writer(graph_file)

                    #Decides which values to write to the .csv file
                    if x_value == "azimuth":
                        if y_value == "avg_number_reflections":
                            #iterates through the dictionary and calculates the avg reflections at the associated angle
                            for key in azimuth_dict.keys():
                                average_refl = azimuth_dict[key][refl_in]/azimuth_dict[key][tot_in]
                                #writes the angles and the calculated value to the .csv file
                                writer.writerow([float(key), float(average_refl)])
                        elif y_value == "absorption_efficiency":
                            #iterates through the dictionary and calculates the absorption efficiency at the associated angle
                            for key in azimuth_dict.keys():
                                abs_eff = float(azimuth_dict[key][abs_in])/float(azimuth_dict[key][tot_in])
                                #writes the angles and the calculated value to the .csv file
                                writer.writerow([float(key), float(abs_eff)])
                    elif x_value == "zenith":
                        #TODO: Add Max power calculation here or a function call to the calculation
                        if y_value == "Max Power":
                            print("create power at max point graph")

                    #closes the graph .csv file and copies it to Most_Recent_Run folder.
                    graph_file.close()
                    copy(output_file_location, self.most_recent_dir)
            else:
                print("++++ERROR++++ The given data file is not a csv file")
        else:
            print("++++ERROR++++ Can't create graphs without all of the required information")

    def write_graph_labels(self, file_location, title="", x_label="", y_label=""):
        """
        This function writes the title and axis labels to a graph's .csv file
        """
        #Opens a .csv file to write to or overwrites an existing file with the same name
        try:
            file_name = open(file_location, 'wb')
        except csv.Error as e:
            print("++++ERROR++++ Couldn't open the csv file. " +
                  "If it is opened in another program, please close it and run the simulation again")
        else:
            #Creates the writer object for a given file
            writer = csv.writer(file_name)
            #Writes the title and axis labels to the file
            writer.writerow([title])
            writer.writerow([x_label, y_label])

    def create_graph(self, folder_location, file_location):
        """
        This function creates a graph from a given .csv file and saves it at the given location
        """
        try:
            file_name = open(file_location, 'rb')
        except csv.Error as e:
            print("++++ERROR++++ Couldn't open the csv file. " +
                  "If it is opened in another program, please close it and run the simulation again")
        else:
            values = []
            #creates the reader object for the file
            reader = csv.reader(file_name)
            #gets the graph's title and axis labels
            title = reader.next()[0]
            axes = reader.next()
            #creates a path to store the graph image
            graph_path = self.file_path_creator(folder_location, title+"_", ".png")
            #defines the graph's title and axis labels
            plt.title(title)
            plt.xlabel(axes[0])
            plt.ylabel(axes[1])
            #reads each row in the file and stores the points to graph in the values list
            for row in reader:
                values.append((float(row[0]), float(row[1])))
            #Sorts the values
            values.sort()
            #plots the points onto the graph
            plt.plot(*zip(*values), marker='o', color='b', ls='-')
            #saves the graph's image
            plt.savefig(graph_path)
            #clears the graph for the next graph
            plt.clf()
            #copies the graph image to the most_recent_run folder
            copy(graph_path, self.most_recent_dir)


    def add_units(self,key_list):
        """
        This function takes in a list of keys, it then goes through the list and adds the correct units to each key.
        It then returns a list with the keys and their corresponding units.
        This it used so the .csv has the unit values in it.
        """

        #the list of key that that have the same units for length
        um_list = ["height", "width", "pitch", "log_pitch", "aspect_ratio"]
        #the list of key that that have the same units for angle
        deg_list = ["zenith", "azimuth"]
        #the list that will be returned
        list_with_units = []
        for value in key_list:
            #keys with their own if statement have their own unique unit value
            if value == "absorption_coefficient":
                list_with_units.append(value+self.abs_coeff_unit_tag)
            elif value == "band_gap":
                list_with_units.append(value+self.band_gap_unit_tag)
            elif value == "absorption_efficiency":
                list_with_units.append(value+self.percent_unit_tag)
            elif value == "wavelength":
                list_with_units.append(value+self.wavelength_unit_tag)
            elif value in deg_list:
                list_with_units.append(value+self.angle_unit_tag)
            elif value in um_list:
                list_with_units.append(value+self.distance_unit_tag)
            else:
                #This adds the keys that don't have units to the list
                list_with_units.append(value)
        return list_with_units

    def remove_units(self,key_list):
        """
        This function takes in a list and the traverses through the list and removes the units attached to a key using
        regex. It then returns a list without the units in the key name. This makes it easier to reference a key.
        """
        for index in range(len(key_list)):
            #Gets the key without the units
            label = match(r'[a-zA-z]*', key_list[index])
            #Replaces the old values
            key_list[index] = label.group()
        return key_list
