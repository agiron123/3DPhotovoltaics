import csv
##import os this can be used later if csv files with the same name already exist
import matplotlib.pyplot as plt

class Analysis(object):
    """Used to output information from the simulation. Has access to all of the information held in
        Statistics. This information can be outputted in raw form, or analyzed further, including transformation
        into graphs and figures. Methods for generating output in various forms are passed using functions as first
        class objects at the time of instantiation """

    def __init__(self, generate_graphs, generate_output):
        """Bind the functions passed in too the Analysis object"""
        Analysis.generate_graphs = generate_graphs
        Analysis.generate_output = generate_output

<<<<<<< Updated upstream
    def generate_output(self, statistics):
        data = statistics.data
        filename = csv.open('Simulation_Data.csv','wb')
        writer = csv.writer(filename)
        writer.writerow(data.keys())
        writer.writerow(data.values())

        writer.writerow("Stats")
        stat_list = statistics.stat_list
        #TODO: dump the data from a statlist

        filename.close()
=======
    #This method creates a CSV file with all of the data from a simulation
    def generate_output(self, statistic):
        #Copies the data dictionary from a statistic
        data = statistic.data

        #Creates a CSV file to write to or overwrites an existing file with the same name
        file_name = open('Simulation_Data.csv', 'wb')

        #Creates the writer object for a given file
        writer = csv.writer(file_name)

        #Write the string to the first row of the CSV file
        writer.writerow(["Compiled Data"])

        #Writes the keys of the data dictionary to the second row of the CSV file
        writer.writerow(data.keys())
        #Writes the values of the data dictionary to the third row of the CSV file
        writer.writerow(data.values())

        #Writes the word "Stats" to the fourth row of the CSV file
        writer.writerow(["Stats"])

        #Copies the stat_list from statistics
        stat_list = statistic.stat_list

        #This will up date each stat's dictionary and then print its contents in the CSV file
        for stat in stat_list:
            stat_dictionary = stat.update_dictionary()
            writer.writerow(stat_dictionary.keys())
            writer.writerow(stat_dictionary.values())

        #Closes the CSV file
        file_name.close()
>>>>>>> Stashed changes


    def generate_graphs(self, statistics):
        #TODO: check the types of desired graphs and how to graph them
