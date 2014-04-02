class GraphSettings(object):
    """Class for the GraphSettings that were parsed from the XML file."""
    def __init__(self, d):
        self.MaxPointPowerVsZenithAngle = "MaxPointPowerVsZenithAngle" in d['output_settings']['graph_settings']
        self.AverageReflectionsVsAzimuthal = "AverageReflectionsVsAzumithal" in d['output_settings']['graph_settings']
        self.AbsorptionEfficiencyVsAzimuthal = "AbsorptionEfficiencyVsAzumithal" in d['output_settings']['graph_settings']
        self.AspectRatioVsAverageReflections = "AspectRatioVsAverageReflections" in d['output_settings']['graph_settings']
        self.IntegratedAreaRatioVsAvgNumReflections = "IntegratedAreaRatioVsAvgNumReflections" in d['output_settings']['graph_settings']
        self.PowerRatio3DVsAbsorbance = "PowerRatio3DVsAbsorbance" in d['output_settings']['graph_settings']
        self.AvgInteractionsVsTowerSpacingLog = "AvgInteractionsVsTowerSpacingLog" in d['output_settings']['graph_settings']
        self.AvgReflectionsVsTowerHeight = "AvgReflectionsVsTowerHeight" in d['output_settings']['graph_settings']