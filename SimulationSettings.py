class SimulationSettings(object):
    """Class to hold the SimulationSettings that were parsed from the XML file."""
    def __init__(self, settingsDict):
        self.materialProfile = settingsDict["Material_profile"]
        self.tower = settingsDict["Tower"]
        self.orbitalProperties = settingsDict["Orbital_Properties"]
        self.simple_orbital_properties = settingsDict["Simple_Orbital_Properties"]
        self.specularReflection = settingsDict["Specular_Reflection"]
        self.opticalMaterial = settingsDict["Optical_Material"]
