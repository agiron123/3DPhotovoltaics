class GraphSettings(object):
    """Class for the GraphSettings that were parsed from the XML file."""
    def __init__(self, settingsDict):
        self.MaxPointPowerVsZenithAngle = settingsDict["MaxPointPowerVsZenithAngle"]
        self.AverageReflectionsVsAzumithal = settingsDict["AverageReflectionsVsAzumithal"]
        self.AbsorptionEfficiencyVsAzumithal = settingsDict["AbsorptionEfficiencyVsAzumithal"]
        self.AspectRatioVsAverageReflections = settingsDict["AspectRatioVsAverageReflections"]
        self.IntegratedAreaRatioVsAvgNumReflections = settingsDict["IntegratedAreaRatioVsAvgNumReflections"]
        self.PowerRatio3DVsAbsorbance = settingsDict["PowerRatio3DVsAbsorbance"]
        self.AvgInteractionsVsTowerSpacingLog = settingsDict["AvgInteractionsVsTowerSpacingLog"]
        self.AvgReflectionsVsTowerHeight = settingsDict["AvgReflectionsVsTowerHeight"]