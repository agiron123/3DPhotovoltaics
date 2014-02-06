class OutputSettings(object):
    """Class for the OutputSettings that were parsed from the XML file."""
    def __init__(self, settingsDict):
        """Get everything from the OutputSettings dictionary"""
        self.powergenratio3D = settingsDict["powergenratio3D"]
        self.maximum_point_power = settingsDict["maximum_point_power"]
        self.absorption_efficiency = settingsDict["absorption_efficiency"]
        self.absorbance = settingsDict["absorbance"]
        self.average_interactions = settingsDict["average_interactions"]
        self.average_reflections = settingsDict["average_reflections"]
        self.integrated_area_ratio = settingsDict["average_area_ratio"]
        self.aspect_ratio = settingsDict["aspect_ratio"]
        self.tower_spacing_log = settingsDict["tower_spacing_log"]
        self.tower_height = settingsDict["tower_height"]
        self.azumithal_angle = settingsDict["azumithal_angle"]

