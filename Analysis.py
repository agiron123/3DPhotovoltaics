class Analysis(object):
    """Used to output information from the simulation. Has access to all of the information held in
        Statistics. This information can be outputted in raw form, or analyzed further, including transformation
        into graphs and figures. Methods for generating output in various forms are passed using functions as first
        class objects at the time of instantiation """

    def __init__(self,generate_graphs,generate_output):
        """Bind the functions passed in too the Analysis object"""
        Analysis.generate_graphs=generate_graphs
        Analysis.generate_output=generate_output

