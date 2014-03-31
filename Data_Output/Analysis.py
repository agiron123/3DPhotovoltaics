import csv
import os
import matplotlib.pyplot as plt
import numpy as np
from re import match, search
from random import *
from shutil import copy
from datetime import datetime


class Analysis(object):
    """Used to output information from the simulation. Has access to all of the information held in
        Statistics. This information can be outputted in raw form, or analyzed further, including transformation
        into graphs and figures. Methods for generating output in various forms are passed using functions as first
        class objects at the time of instantiation """

    #--------------------------------------------------------------------
    #These variables are generic tags used through the this python file
    # they determine the name of files and headers in csv files

    #CSV Headers
    tower_data_tag = "Tower Data"
    compiled_data_tag = "Compiled Data"
    stats_tag = "Stats"
    #Folder names
    output_folder_tag = "Simulation_Data"
    most_recent_tag = "Most_Recent_Run"
    raw_data_tag = "Raw_Data"
    #---------------------------------------------------------------------

    def __init__(self):#, graph_settings):
        """Bind the functions passed in too the Analysis object"""
        self.folder_dir = self.folder_creator(None)
        self.most_recent_dir = self.folder_creator(self.most_recent_tag)
        #self.graph_settings = vars(graph_settings)

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

    #TODO: Add units
    def generate_output(self, statistics, sim_settings, save_path=False):
        """
        This method creates a CSV file with all of the data from a simulation. It takes in  a list of statistics
        and whether or not to save a photon's path, it then generates a csv file for each statistic/simulation
        """
        #The name of the CSV file
        data_file_name = 'Raw_Sim_Data_'
        #The name of the folders for the raw data CSV files
        data_folder_name = self.raw_data_tag

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

        print("Creating Output CSV File\n")

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
            data = statistics[index].data

            #gets the tower's setting from the simulation settings
            tower_settings = vars(sim_settings[index])['tower']

            #---------------------------------------------------------------------------------------
            #TODO: remove print statements and remove the overwrite of tower settings
            # This was for testing when the xml parser did not work to use this you need to comment out the line above
            #print("\n Tower settings changes\n")
            #width = randint(1, 10)*10
            #height = randint(1, 10)*10
            #pitch = randint(1, 10)*10
            #tower_settings = {'width': str(width), 'shape': 'square', 'height': str(height), 'pitch': str(pitch)}
            #----------------------------------------------------------------------------------------

            #adds the aspect ratio and log of the tower pitch to the tower settings
            self.add_tower_info(tower_settings)
            print("\nEnd of Tower Settings Changes\n")

            #Creates the csv file and stores the location for later use
            file_location = self.file_path_creator(self.folder_dir, data_file_name, ".csv")

            #Opens a CSV file to write to or overwrites an existing file with the same name
            try:
                file_name = open(file_location, 'wb')
            except csv.Error as e:
                print("++++ERROR++++ Couldn't open the csv file. "
                      + "If it is opened in another program, please close it and run the program again")
            else:
                #Creates the writer object for a given file
                writer = csv.writer(file_name)

                #Write the string to the first row of the CSV file
                writer.writerow([self.tower_data_tag])

                #Writes the keys of the tower_settings dictionary to the second row of the CSV file
                writer.writerow(tower_settings.keys())
                #Writes the values of the tower_settings dictionary to the third row of the CSV file
                writer.writerow(tower_settings.values())

                #Write the string to the fourth row of the CSV file
                writer.writerow([self.compiled_data_tag])

                #Writes the keys of the data dictionary to the fifth row of the CSV file
                writer.writerow(data.keys())
                #Writes the values of the data dictionary to the sixth row of the CSV file
                writer.writerow(data.values())

                #Writes the word "Stats" to the next row of the CSV file
                writer.writerow([self.stats_tag])

                #Copies the stat_list from statistics
                stat_list = statistics[index].stat_list
                if len(stat_list) != 0:

                    #Gets a stat's dictionary in order to write the stat's attributes to the csv file
                    stat_dict = vars(stat_list[0])
                    if save_path == False and stat_dict.has_key("path"):
                        del stat_dict["path"]
                    writer.writerow(stat_dict.keys())
                    writer.writerow(stat_dict.values())

                    #This will print each stat's contents in the CSV file
                    for stat in stat_list[1:]:
                        stat_dict = vars(stat)
                        if save_path == False and stat_dict.has_key("path"):
                            del stat_dict['path']
                        stat_dict = stat_dict.values()
                        writer.writerow(stat_dict)

                    #Closes the CSV file
                    file_name.close()

                    #Copies the new file to the most_recent_dir folder
                    copy(file_location, self.most_recent_dir)

                    print("Data has been outputted in to a CSV file\n")
                    print("The file location is: " + file_location + "\n")
                else:
                    #close and removes the files since it does not have any data
                    file_name.close()
                    os.remove(file_location)

    def folder_creator(self, folder_name):
        """
        This function creates a folder, with the name taken from folder_name, that stores all of the CSV files for the
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
            pass  # already exist
        return destination_dir


    @staticmethod
    def file_path_creator(destination_dir, file_name, extension):
        """
        This function helps create the CSV file, with the value taken from file_name. To create multiple files for
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
        make a the CSV file used to generate the graph. Finally it calls the function to generate the graph.
        """
        #data_dir = os.path.join(self.folder_dir, self.raw_data_tag)
        data_dir = self.folder_dir
        #checks if there are multiple simulations before creating graph
        print(data_dir)
        if len(os.listdir(data_dir)) > 1:
            settings_dict = vars(graph_settings)
            if settings_dict["MaxPointPowerVsZenithAngle"] == True:
                output_dir = self.folder_creator("Max_Point_Power_vs_Zenith_Angle")
                file_location = self.file_path_creator(output_dir, "Max_Point_Power_vs_Zenith_", ".csv")
                #TODO: finish implementing
                #self.max_power_vs_zenith(file_location)

            if settings_dict["AverageReflectionsVsAzimuthal"] == True:
                output_dir = self.folder_creator("Average_Reflections_vs_Azimuth_Angle")
                file_location = self.file_path_creator(output_dir, "Avg_Reflections_vs_Azimuthal_", ".csv")
                #TODO: finish implementing
                #self.avg_reflections_vs_azimuthal(file_location)
                #self.create_graph(output_dir, file_location)

            if settings_dict["AbsorptionEfficiencyVsAzimuthal"] == True:
                output_dir = self.folder_creator("Absorption_Efficiency_vs_Azimuth_Angle")
                file_location = self.file_path_creator(output_dir, "Absorption_Efficiency_vs_Azimuthal_", ".csv")
                #TODO: finish implementing
                #self.absorption_efficiency_vs_azimuthal(file_location)
                #self.create_graph(output_dir, file_location)

            if settings_dict["AspectRatioVsAverageReflections"] == True:
                output_dir = self.folder_creator("Aspect_Ratio_vs_Average_Number_of_Reflections")
                file_location = self.file_path_creator(output_dir, "Aspect_Ratio_vs_Avg_Reflections_", ".csv")
                self.aspect_ratio_vs_avg_reflections(file_location)
                self.create_graph(output_dir, file_location)

            if settings_dict["IntegratedAreaRatioVsAvgNumReflections"] == True:
                output_dir = self.folder_creator("Integrated_Area_Ratio_vs_Avg_Num_Reflections")
                file_location = self.file_path_creator(output_dir, "Integrated_Area_Ratio_vs_Avg_Num_Reflections_", ".csv")
                #TODO: finish implementing
                #self.integrated_area_ratio_vs_avg_num_reflections(file_location)

            if settings_dict["PowerRatio3DVsAbsorbance"] == True:
                output_dir = self.folder_creator("Power_Ratio_3D_vs_Absorbance")
                file_location = self.file_path_creator(output_dir, "Power_Ratio_3D_vs_Absorbance_", ".csv")
                #TODO: finish implementing
                #self.power_ratio_vs_absorbance(file_location)

            if settings_dict["AvgInteractionsVsTowerSpacingLog"] == True:
                output_dir = self.folder_creator("Average_Number_of_Interactions_vs_Tower_Pitch_Log")
                file_location = self.file_path_creator(output_dir, "Avg_Interactions_vs_Tower_Pitch_Log_", ".csv")
                self.avg_interactions_vs_tower_spacing(file_location)
                self.create_graph(output_dir, file_location)

            if settings_dict["AvgReflectionsVsTowerHeight"] == True:
                output_dir = self.folder_creator("Average_Number_of_Reflections_vs_Tower_Height")
                file_location = self.file_path_creator(output_dir, "Avg_Reflections_vs_Tower_Height_", ".csv")
                self.avg_reflections_vs_tower_height(file_location)
                self.create_graph(output_dir, file_location)
        else:
            print("Need to run more simulations before being able to create a graph")

    def read_simulation_data(self, data_directory, file_location, x_value="", y_value="", tower_val=False):
        """
        This function creates the csv file needed to create a graph. It takes in the x and y values, the it goes through
        the files in the given directory and pulls out the data for the x and y value. It then writes it to a csv file
        and stores it at the given file location. tower_val is a boolean used to state whether the x_value is a tower
        property
        """
        #opens the graph CSV file to be appended to
        try:
            graph_file = open(file_location, 'ab')
        except csv.Error as e:
            print("++++ERROR++++ Couldn't open the csv file. "
                  + "If it is opened in another program, please close it and run the program again")
        #creates writer object
        writer = csv.writer(graph_file)

        #Looks through all of the files in the given data_directory and opens CSV files for reading
        for files in os.listdir(data_directory):
            if files.endswith(".csv"):
                file_dir = os.path.join(data_directory, files)
                try:
                    file_name = open(file_dir, 'rb')
                except csv.Error as e:
                    print("++++ERROR++++ Couldn't open the csv file. "
                          + "If it is opened in another program, please close it and run the program again")
                reader = csv.reader(file_name)

                #gets the first line in the CSV file
                data_type = reader.next()
                #checks tower_val to determine whether or not to get the tower data
                if tower_val == True:
                    #gets the tower data
                    if data_type[0] == self.tower_data_tag:
                        tower_keys = reader.next()
                        tower_values = reader.next()
                    else:
                        while data_type[0] != self.tower_data_tag:
                            data_type = reader.next()
                        tower_keys = reader.next()
                        tower_values = reader.next()

                #Gets the Compiled Data
                if data_type[0] == self.compiled_data_tag:
                    keys = reader.next()
                    values = reader.next()
                else:
                    while data_type[0] != self.compiled_data_tag:
                        data_type = reader.next()
                    keys = reader.next()
                    values = reader.next()

                file_name.close()

                #Gets the index of the desired y_value
                try:
                    y = keys.index(y_value)
                except ValueError as e:
                    print("The"+y_value+"is not in"+self.compiled_data_tag+
                          "Check if you are looking for the correct value and in the correct list")

                if tower_val == True:
                    #Gets the index of the desired x_value and then writes the data point to the graph CSV file
                    try:
                        x = tower_keys.index(x_value)
                    except ValueError as e:
                        print("The"+x_value+"is not in"+self.tower_data_tag+
                              "Check if you are looking for the correct value and in the correct list")
                    writer.writerow([float(tower_values[x]), float(values[y])])
                else:
                    try:
                        x = keys.index(x_value)
                    except ValueError as e:
                        print("The"+x_value+"is not in"+self.compiled_data_tag+
                              "Check if you are looking for the correct value and in the correct list")
                    writer.writerow([float(values[x]), float(values[y])])
        #closes the graph CSV file and copies it to Most_Recent_Run folder.
        graph_file.close()
        copy(file_location, self.most_recent_dir)

    #TODO: check the types of desired graphs and how to graph them
    def max_power_vs_zenith(self, file_location):
        #TODO: finish implementing
        print("generate_graphs in Analysis.py is not fully implemented yet."
              +"\nCannot create Max Power vs Zenith Angle graph\n")
        #raise NotImplementedError("generate_graphs in Analysis.py is not fully implemented yet.")

    def avg_reflections_vs_azimuthal(self, file_location):
        title = "Average Number of Reflections vs Azimuthal Angle"
        x_label = "Azimuthal Angle (Degrees)"
        y_label = "Average Number of Reflections"
        #TODO: finish implementing
        print("generate_graphs in Analysis.py is not fully implemented yet."
              + "\nCannot create Average Number of Reflections vs Azimuthal Angle graph\n")
        #raise NotImplementedError("generate_graphs in Analysis.py is not fully implemented yet.")
        #self.write_graph_labels(file_location, title, x_label, y_label)
        #self.read_simulation_data(self.folder_dir, file_location, "avg_azimuth", "avg_number_reflections")

    def absorption_efficiency_vs_azimuthal(self, file_location):
        title = "Absorption Efficiency vs Azimuthal Angle"
        x_label = "Azimuthal Angle (Degrees)"
        y_label = "Absorption Efficiency"
        #TODO: finish implementing
        print("generate_graphs in Analysis.py is not fully implemented yet."
              +"\nCannot create Absorption Efficiency vs Azimuthal Angle graph\n")
        #raise NotImplementedError("generate_graphs in Analysis.py is not fully implemented yet.")
        #self.write_graph_labels(file_location, title, x_label, y_label)
        #self.read_simulation_data(self.folder_dir, file_location, "avg_azimuth", "absorption_efficiency")

    def aspect_ratio_vs_avg_reflections(self, file_location):
        title = "Aspect Ratio vs Average Number of Reflections"
        x_label = "Aspect Ration (microns)"
        y_label = "Average Number of Reflections"
        self.write_graph_labels(file_location, title, x_label, y_label)
        self.read_simulation_data(self.folder_dir, file_location, "aspect_ratio", "avg_number_reflections", True)

    def integrated_area_ratio_vs_avg_num_reflections(self, file_location):
        #TODO: finish implementing
        print("generate_graphs in Analysis.py is not fully implemented yet."
              + "\n Cannot create Integrated Area Ratio vs Avgerage Number of Reflections graph\n")
        #raise NotImplementedError("generate_graphs in Analysis.py is not fully implemented yet.")

    def power_ratio_vs_absorbance(self, file_location):
        #TODO: finish implementing
        print("generate_graphs in Analysis.py is not fully implemented yet. "
              + "\n Cannot create Power Ratio vs Absorbance graph\n")
        #raise NotImplementedError("generate_graphs in Analysis.py is not fully implemented yet.")

    def avg_interactions_vs_tower_spacing(self, file_location):
        title = "Average Number of Interactions vs Tower Pitch"
        x_label = "Tower Pitch (microns)"
        y_label = "Average Number of Interactions"
        self.write_graph_labels(file_location, title, x_label, y_label)
        self.read_simulation_data(self.folder_dir, file_location, "pitch", "avg_number_interactions", True)

    def avg_reflections_vs_tower_height(self, file_location):
        title = "Average Number of Reflections vs Tower Height"
        x_label = "Tower Height (microns)"
        y_label = "Average Number of Reflections"
        self.write_graph_labels(file_location, title, x_label, y_label)
        self.read_simulation_data(self.folder_dir, file_location, "height", "avg_number_reflections", True)

    def add_tower_info(self, tower_settings):
        """
        This function taking in tower settings dictionary and adds the aspect ration and log of the tower pitch
        """
        tower_settings["aspect_ratio"] = float(tower_settings['width'])/float(tower_settings['height'])
        tower_settings["log_pitch"] = np.log(float(tower_settings['pitch']))

    def write_graph_labels(self, file_location, title="", x_label="", y_label=""):
        """
        This function writes the title and axis labels to a graph's csv file
        """
        #Opens a CSV file to write to or overwrites an existing file with the same name
        try:
            file_name = open(file_location, 'wb')
        except csv.Error as e:
            print("++++ERROR++++ Couldn't open the csv file. "
                  + "If it is opened in another program, please close it and run the program again")
        else:
            #Creates the writer object for a given file
            writer = csv.writer(file_name)
            #Writes the title and axis labels to the file
            writer.writerow([title])
            writer.writerow([x_label, y_label])

    def create_graph(self, folder_location, file_location):
        """
        This function creates a graph from a given csv file and saves it at the given location
        """
        try:
            file_name = open(file_location, 'rb')
        except csv.Error as e:
            print("++++ERROR++++ Couldn't open the csv file. "
                  + "If it is opened in another program, please close it and run the program again")
        else:
            values = []
            #creates the reader object for the file
            reader = csv.reader(file_name)
            #gets the graph's title and axis labels
            title = reader.next()[0]
            axes = reader.next()
            #creates a path the store the graph image
            graph_path = self.file_path_creator(folder_location, title+"_", ".png")
            #defines the graph's title and axis labels
            plt.title(title)
            plt.xlabel(axes[0])
            plt.ylabel(axes[1])
            #reads each row in the file and store the points to graph in the values list
            for row in reader:
                values.append((float(row[0]), float(row[1])))
            #Sorts values
            values.sort()
            #plots the points onto the graph
            plt.plot(*zip(*values), marker='o', color='b', ls='-')
            #saves the graph's images
            plt.savefig(graph_path)
            #clears the graph for the next graph
            plt.clf()
            #copies the graph image to the most recent run folder
            copy(graph_path, self.most_recent_dir)
