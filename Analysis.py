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

    def __init__(self):#, graph_settings):
        """Bind the functions passed in too the Analysis object"""
        self.folder_dir = ''
        self.most_recent_dir = ''
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
        file_location = self.file_creator(self.folder_dir, data_file_name)
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
        data_folder_name = 'Raw Data'
        most_recent_dir_name = 'Most_Recent_Run'
        #Creates the folders
        self.folder_dir = self.folder_creator(data_folder_name)
        self.most_recent_dir = self.folder_creator(most_recent_dir_name)

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
            file_location = self.file_creator(self.folder_dir, data_file_name)

            #Creates a CSV file to write to or overwrites an existing file with the same name
            try:
                file_name = open(file_location, 'wb')
            except csv.Error as e:
                print("++++ERROR++++ Couldn't open the csv file. If it is opened in another program, please close it and run the program again")
            else:
                #Creates the writer object for a given file
                writer = csv.writer(file_name)

                #Write the string to the first row of the CSV file
                writer.writerow(["Tower Data"])

                #Writes the keys of the tower_settings dictionary to the second row of the CSV file
                writer.writerow(tower_settings.keys())
                #Writes the values of the tower_settings dictionary to the third row of the CSV file
                writer.writerow(tower_settings.values())

                #Write the string to the fourth row of the CSV file
                writer.writerow(["Compiled Data"])

                #Writes the keys of the data dictionary to the fifth row of the CSV file
                writer.writerow(data.keys())
                #Writes the values of the data dictionary to the sixth row of the CSV file
                writer.writerow(data.values())

                #Writes the word "Stats" to the next row of the CSV file
                writer.writerow(["Stats"])

                #Copies the stat_list from statistics
                stat_list = statistics[index].stat_list
                if len(stat_list) != 0:
                    #Gets the dictionary keys in order the write the stat's attributes to the csv file
                    writer.writerow(vars(stat_list[0]).keys())

                    #This will up date each stat's dictionary and then print its contents in the CSV file
                    for stat in stat_list:
                        if save_path == True:
                            writer.writerow(vars(stat).values())
                        else:
                            writer.writerow(vars(stat).values()[:-1])
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
    @staticmethod
    def folder_creator(folder_name):
        #gets the currents scripts directory
        script_dir = os.path.dirname(os.path.abspath(__file__))
        #adds the new folder to the directory
        destination_dir = os.path.join(script_dir, "Simulation Data", folder_name)
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
    def file_creator(destination_dir, file_name):
        sim_number = 0
        #checks the folder for previous data files and determines the current simulation number
        for files in os.listdir(destination_dir):
            if files.endswith(".csv") and (match(r'[^0-9]*', files).group() == file_name):
                file_number = int(search(r'\d+', files).group())
                if file_number >= sim_number:
                    sim_number = file_number+1
        #creates the final file name
        new_file_name = file_name + str(sim_number) + '.csv'
        #creates the path to the new data file
        path = os.path.join(destination_dir, new_file_name)
        return path

    def generate_graphs(self, graph_settings):
        settings_dict = vars(graph_settings)

        if settings_dict["MaxPointPowerVsZenithAngle"] == True:
            self.max_power_vs_zenith(self.folder_dir)

        if settings_dict["AverageReflectionsVsAzumithal"] == True:
            self.avg_reflections_vs_azumithal(self.folder_dir)

        if settings_dict["AbsorptionEfficiencyVsAzumithal"] == True:
            self.absorption_efficiency_vs_azumithal(self.folder_dir)

        if settings_dict["AspectRatioVsAverageReflections"] == True:
            self.aspect_ratio_vs_avg_reflections(self.folder_dir)

        if settings_dict["IntegratedAreaRatioVsAvgNumReflections"] == True:
            self.integrated_area_ratio_vs_avg_num_reflections(self.folder_dir)

        if settings_dict["PowerRatio3DVsAbsorbance"] == True:
            self.power_ratio_vs_absorbance(self.folder_dir)

        if settings_dict["AvgInteractionsVsTowerSpacingLog"] == True:
            self.avg_interactions_vs_tower_spacing(self.folder_dir)

        if settings_dict["AvgReflectionsVsTowerHeight"] == True:
            self.avg_reflections_vs_tower_height(self.folder_dir)

        raise NotImplementedError("generate_graphs in Analysis.py is not fully implemented yet.")

    #TODO: change the default x and y values to ""
    def read_files(self, folder_directory, x_value="", y_value=""):
        print(folder_directory)
        fol_dir = ''
        plot_x = []
        plot_y = []
        for files in os.listdir(folder_directory):
            fol_dir = os.path.join(folder_directory, files)
            try:
                file_name = open(fol_dir, 'rb')
            except csv.Error as e:
                print("++++ERROR++++ Couldn't open the csv file. If it is opened in another program, please close it and run the program again")
            reader = csv.reader(file_name)
            data_type = reader.next()
            keys = reader.next()
            values = reader.next()
            try:
                x = keys.index(x_value)
            except ValueError as e:
                print("The X value is not in the list. Check if you are looking for the correct value and in the correct list")
            try:
                y = keys.index(y_value)
            except ValueError as e:
                print("The Y value is not in the list. Check if you are looking for the correct value and in the correct list")
            plot_x.append(float(values[x]))
            plot_y.append(float(values[y]))
##            print(data_type)
##            print(keys)
##            print(values)
##            attributes = list(reader)
##            print(attributes[0])
##            print(reader.next())
            file_name.close()
##            plt.show()
##            break
##            plt.plot(float(values[0]),float(values[2]))
        plt.plot(plot_x, plot_y, color='b', marker='o', linestyle='-')
        plt.ylabel(y_value)
        plt.xlabel(x_value)
        plt.show()


    #TODO: check the types of desired graphs and how to graph them
    def max_power_vs_zenith(self, folder_directory):
        raise NotImplementedError("generate_graphs in Analysis.py is not fully implemented yet.")

    def avg_reflections_vs_azumithal(self, folder_directory):
        raise NotImplementedError("generate_graphs in Analysis.py is not fully implemented yet.")

    def absorption_efficiency_vs_azumithal(self, folder_directory):
        raise NotImplementedError("generate_graphs in Analysis.py is not fully implemented yet.")

    def aspect_ratio_vs_avg_reflections(self, folder_directory):
        raise NotImplementedError("generate_graphs in Analysis.py is not fully implemented yet.")

    def integrated_area_ratio_vs_avg_num_reflections(self, folder_directory):
        raise NotImplementedError("generate_graphs in Analysis.py is not fully implemented yet.")

    def power_ratio_vs_absorbance(self, folder_directory):
        raise NotImplementedError("generate_graphs in Analysis.py is not fully implemented yet.")

    def avg_interactions_vs_tower_spacing(self, folder_directory):
        raise NotImplementedError("generate_graphs in Analysis.py is not fully implemented yet.")

    def avg_reflections_vs_tower_height(self, folder_directory):
        raise NotImplementedError("generate_graphs in Analysis.py is not fully implemented yet.")

    #This function taking in tower settings dictionary and adds the aspect ration and log of the tower pitch
    def add_tower_info(self, tower_settings):
        tower_settings["aspect_ratio"] = float(tower_settings['width'])/float(tower_settings['height'])
        tower_settings["log_pitch"] = np.log(float(tower_settings['pitch']))