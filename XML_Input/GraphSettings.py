"""Holds the GraphSettings class"""
class GraphSettings(object):
    """Class for the GraphSettings that were parsed from the XML file."""
    def __init__(self, d):
        """
        Initialize the graph settings object with the given dictionary, essentially just copy everything over
        @type d: dictionary
        @param d: dictionary containing all the info needed for initialization
        """
        self.MaxPointPowerVsZenithAngle = "MaxPointPowerVsZenithAngle" in d['output_settings']['graph_settings']
        self.AverageReflectionsVsAzimuthal = "AverageReflectionsVsAzumithal" in d['output_settings']['graph_settings']
        self.AbsorptionEfficiencyVsAzimuthal = "AbsorptionEfficiencyVsAzumithal" in d['output_settings']['graph_settings']
        self.AspectRatioVsAverageReflections = "AspectRatioVsAverageReflections" in d['output_settings']['graph_settings']
        self.IntegratedAreaRatioVsAvgNumReflections = "IntegratedAreaRatioVsAvgNumReflections" in d['output_settings']['graph_settings']
        self.PowerRatio3DVsAbsorbance = "PowerRatio3DVsAbsorbance" in d['output_settings']['graph_settings']
        self.AvgInteractionsVsTowerSpacingLog = "AvgInteractionsVsTowerSpacingLog" in d['output_settings']['graph_settings']
        self.AvgReflectionsVsTowerHeight = "AvgReflectionsVsTowerHeight" in d['output_settings']['graph_settings']