import csv
import os
import matplotlib.pyplot as plt
import numpy as np
from re import match, search
from shutil import copy



class Analysis(object):
    """Used to output information from the simulation. Has access to all of the information held in
        Statistics. This information can be outputted in raw form, or analyzed further, including transformation
        into graphs and figures. Methods for generating output in various forms are passed using functions as first
        class objects at the time of instantiation """

    tower_data_tag = "Tower Data"
    compiled_data_tag = "Compiled Data"
    stats_tag = "Stats"
    output_folder_tag = "Simulation Data"
    most_recent_tag = "Most_Recent_Run"
    raw_data_tag = "Raw Data"

    def __init__(self):#, graph_settings):
        """Bind the functions passed in too the Analysis object"""
        self.folder_dir = self.folder_creator(None)
        self.most_recent_dir = self.folder_creator(self.most_recent_tag)
        #self.graph_settings = vars(graph_settings)

    """This function creates csv files that save only a photon's path. This is only for debugging"""
    def save_photon_path(self, statistic):
        #gets the statistic's data
        data = statistic.data
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

    """This method creates a CSV file with all of the data from a simulation. It takes in  a list of statistics
    and whether or not to save a photon's path, it then generates a csv file for each statistic/simulation"""
    def generate_output(self, statistics, sim_settings, save_path=True):
        #The name of the CSV file
        data_file_name = 'Raw_Simulation_Data_'
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

        if len(statistics) != len(sim_settings):
            raise ValueError("Number of statistics doesn't match number of simulations settings. Should be equal")

        #This for loop allows it to output data for multiple simulations
        for index in range(len(statistics)):
            #Copies the data dictionary from a statistic
            data = statistics[index].data

            #gets the tower's setting from the simulation settings
            tower_settings = vars(sim_settings[index])['tower']
            #TODO: remove print statements and remove the overwrite of tower settings
            print("\n Tower settings changes\n")
            tower_settings = {'width': '4', 'shape': 'square', 'height': '4' , 'pitch': '4'}
            #adds the aspect ratio and log of the tower pitch to the tower settings
            self.add_tower_info(tower_settings)
            print("\nEnd of Tower Settings Changes\n")

            #Creates the csv file and stores the location for later use
            file_location = self.file_path_creator(self.folder_dir, data_file_name, ".csv")

            #Opens a CSV file to write to or overwrites an existing file with the same name
            try:
                file_name = open(file_location, 'wb')
            except csv.Error as e:
                print("++++ERROR++++ Couldn't open the csv file. If it is opened in another program, please close it and run the program again")
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

                    #Gets the dictionary keys in order the write the stat's attributes to the csv file
                    stat_dict = vars(stat_list[0])
                    if save_path != True:
                        del stat_dict["path"]
                    writer.writerow(stat_dict.keys())
                    writer.writerow(stat_dict.values())

                    #This will up date each stat's dictionary and then print its contents in the CSV file
                    for stat in stat_list[1:]:
                        stat_dict = vars(stat)
                        if save_path != True:
                            del stat_dict["path"]
                        stat_dict = stat_dict.values()
                        writer.writerow(stat_dict)

                    #Closes the CSV file
                    file_name.close()

                    #Copies the new file to the most_recent_dir folder
                    copy(file_location, self.most_recent_dir)

                    print("Data has been outputted in to a CSV file\n")
                    print("The file location is: " + file_location + "\n")
                else:
                    file_name.close()
                    os.remove(file_location)

    """ This function creates a folder, with the name taken from folder_name, that stores all of the CSV files for the
        output function. It also creates the path to that folder and returns the path"""
    def folder_creator(self, folder_name):
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

    """ This function helps create the CSV file, with the value taken from file_name. To create multiple files for
        different runs, this function uses regex to check the files in the directory to determine the number of
        the most recent run and then increments it by 1. It then returns the path to the file"""
    @staticmethod
    def file_path_creator(destination_dir, file_name, extension):
        sim_number = 0
        #checks the folder for previous data files and determines the current simulation number
        for files in os.listdir(destination_dir):
            if files.endswith(extension) and (match(r'[^0-9]*', files).group() == file_name):
                file_number = int(search(r'\d+', files).group())
                if file_number >= sim_number:
                    sim_number = file_number+1
        #creates the final file name
        if sim_number<10:
            sim_number = "0"+str(sim_number)
        else:
            sim_number = str(sim_number)
        new_file_name = file_name + sim_number + extension
        #creates the path to the new data file
        path = os.path.join(destination_dir, new_file_name)
        return path

    def generate_graphs(self, graph_settings):
        settings_dict = vars(graph_settings)
        if settings_dict["MaxPointPowerVsZenithAngle"] == 'True':
            self.folder_creator("Max_Point_Power_vs_Zenith Angle")
            #self.max_power_vs_zenith(self.folder_dir)

        if settings_dict["AverageReflectionsVsAzumithal"] == 'True':
            output_dir = self.folder_creator("Average_Reflections_vs_Azumithal")
            file_location = self.file_path_creator(output_dir, "AverageReflectionsVsAzumithal_", ".csv")
            self.avg_reflections_vs_azumithal(file_location)
            self.create_graph(output_dir, file_location)

        if settings_dict["AbsorptionEfficiencyVsAzumithal"] == 'True':
            output_dir = self.folder_creator("Absorption_Efficiency_vs_Azumithal")
            file_location = self.file_path_creator(output_dir, "AbsorptionEfficiencyVsAzumithal_", ".csv")
            self.absorption_efficiency_vs_azumithal(file_location)
            self.create_graph(output_dir, file_location)
            #self.absorption_efficiency_vs_azumithal(self.folder_dir)

        if settings_dict["AspectRatioVsAverageReflections"] == 'True':
            output_dir = self.folder_creator("Aspect_Ratio_vs_Average_Reflections")
            file_location = self.file_path_creator(output_dir, "AspectRatioVsAverageReflections_", ".csv")
            self.aspect_ratio_vs_avg_reflections(file_location)
            self.create_graph(output_dir, file_location)
            #self.aspect_ratio_vs_avg_reflections(self.folder_dir)

        if settings_dict["IntegratedAreaRatioVsAvgNumReflections"] == 'True':
            self.folder_creator("Integrated_Area_Ratio_vs_Avg_Num_Reflections")
            #self.integrated_area_ratio_vs_avg_num_reflections(self.folder_dir)

        if settings_dict["PowerRatio3DVsAbsorbance"] == 'True':
            self.folder_creator("Power_Ratio_3D_vs_Absorbance")
            #self.power_ratio_vs_absorbance(self.folder_dir)

        if settings_dict["AvgInteractionsVsTowerSpacingLog"] == 'True':
            self.folder_creator("Avg_Interactions_vs_Tower_Spacing_Log")
            #self.avg_interactions_vs_tower_spacing(self.folder_dir)

        if settings_dict["AvgReflectionsVsTowerHeight"] == 'True':
            self.folder_creator("Avg_Reflections_vs_Tower_Height")
            #self.avg_reflections_vs_tower_height(self.folder_dir)

        #raise NotImplementedError("generate_graphs in Analysis.py is not fully implemented yet.")

    def read_simulation_data(self, data_directory, file_location, x_value="", y_value=""):
        if os.listdir(data_directory) != []:
            file_dir = ''
            try:
                graph_file = open(file_location, 'ab')
            except csv.Error as e:
                print("++++ERROR++++ Couldn't open the csv file. If it is opened in another program, please close it and run the program again")
            writer = csv.writer(graph_file)
            for files in os.listdir(data_directory):
                if files.endswith(".csv"):
                    file_dir = os.path.join(data_directory, files)
                    try:
                        file_name = open(file_dir, 'rb')
                    except csv.Error as e:
                        print("++++ERROR++++ Couldn't open the csv file. If it is opened in another program, please close it and run the program again")
                    reader = csv.reader(file_name)

                    data_type = reader.next()
                    while data_type[0] != self.compiled_data_tag:
                        data_type = reader.next()

                    #Wanted compiled data
                    keys = reader.next()
                    values = reader.next()

                    file_name.close()

                    try:
                        x = keys.index(x_value)
                    except ValueError as e:
                        print("The X value is not in the list. Check if you are looking for the correct value and in the correct list")
                    try:
                        y = keys.index(y_value)
                    except ValueError as e:
                        print("The Y value is not in the list. Check if you are looking for the correct value and in the correct list")
                    writer.writerow([float(values[x]),float(values[y])])
            graph_file.close()
            copy(file_location, self.most_recent_dir)

    #TODO: check the types of desired graphs and how to graph them
    def max_power_vs_zenith(self, file_location):
        raise NotImplementedError("generate_graphs in Analysis.py is not fully implemented yet.")

    def avg_reflections_vs_azumithal(self, file_location):
        title = "Average Number of Reflections vs Azumithal Angle"
        x_label = "Azumithal Angle (Degrees)"
        y_label = "Average Number of Reflections"
        self.write_graph_labels(file_location, title, x_label, y_label)
        self.read_simulation_data(self.folder_dir, file_location, "avg_azimuth", "avg_number_reflections")

    def absorption_efficiency_vs_azumithal(self, file_location):
        title = "Absorption Efficiency vs Azumithal Angle"
        x_label = "Azumithal Angle (Degrees)"
        y_label = "Absorption Efficiency"
        self.write_graph_labels(file_location, title, x_label, y_label)
        self.read_simulation_data(self.folder_dir, file_location, "avg_azimuth", "absorption_efficiency")
        #raise NotImplementedError("generate_graphs in Analysis.py is not fully implemented yet.")

    def aspect_ratio_vs_avg_reflections(self, file_location):
        title = "Aspect Ratio vs Average Number of Reflections"
        x_label = "Aspect Ration (microns)"
        y_label = "Average Number of Reflections"
        self.write_graph_labels(file_location, title, x_label, y_label)
        self.read_simulation_data(self.folder_dir, file_location, "aspect_ratio", "avg_number_reflections")
        #raise NotImplementedError("generate_graphs in Analysis.py is not fully implemented yet.")

    def integrated_area_ratio_vs_avg_num_reflections(self, file_location):
        raise NotImplementedError("generate_graphs in Analysis.py is not fully implemented yet.")

    def power_ratio_vs_absorbance(self, file_location):
        raise NotImplementedError("generate_graphs in Analysis.py is not fully implemented yet.")

    def avg_interactions_vs_tower_spacing(self, file_location):
        raise NotImplementedError("generate_graphs in Analysis.py is not fully implemented yet.")

    def avg_reflections_vs_tower_height(self, file_location):
        raise NotImplementedError("generate_graphs in Analysis.py is not fully implemented yet.")

    """This function taking in tower settings dictionary and adds the aspect ration and log of the tower pitch"""
    def add_tower_info(self, tower_settings):
        tower_settings["aspect_ratio"] = float(tower_settings['width'])/float(tower_settings['height'])
        tower_settings["log_pitch"] = np.log(float(tower_settings['pitch']))

    def write_graph_labels(self, file_location, title="", x_label="", y_label=""):
        #Opens a CSV file to write to or overwrites an existing file with the same name
        try:
            file_name = open(file_location, 'wb')
        except csv.Error as e:
            print("++++ERROR++++ Couldn't open the csv file. If it is opened in another program, please close it and run the program again")
        else:
            #Creates the writer object for a given file
            writer = csv.writer(file_name)
            #Write the string to the first row of the CSV file
            writer.writerow([title])
            writer.writerow([x_label, y_label])

    def create_graph(self, folder_location, file_location):
        try:
            file_name = open(file_location, 'rb')
        except csv.Error as e:
            print("++++ERROR++++ Couldn't open the csv file. If it is opened in another program, please close it and run the program again")
        else:
            #Creates the writer object for a given file
            values = []
            reader = csv.reader(file_name)
            title = reader.next()[0]
            axes = reader.next()

            graph_path = self.file_path_creator(folder_location, title+"_", ".png")

            plt.title(title)
            plt.xlabel(axes[0])
            plt.ylabel(axes[1])
            for row in reader:
                values.append((float(row[0]), float(row[1])))
            values.sort()
            plt.plot(*zip(*values), marker='o', color='b', ls='-')
            plt.savefig(graph_path)
            plt.clf()
            plt.cla()
            plt.close()
            copy(graph_path, self.most_recent_dir)
