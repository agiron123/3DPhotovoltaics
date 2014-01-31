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


    def generate_graphs(self, statistics):
    #TODO: check the types of desired graphs and how to graph them
