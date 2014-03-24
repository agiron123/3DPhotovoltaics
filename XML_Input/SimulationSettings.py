class SimulationSettings(object):
    """Class to hold the SimulationSettings that were parsed from the XML file."""

    def __init__(self, settings_dict):
        """
        Create the simulation settings object using the given dictionary.
        The dictionary is passed from the XML parser.
        """
        self.materialProfile = settings_dict["Material_Profile"]
        self.tower = settings_dict["Tower"]
        self.orbitalProperties = settings_dict["Orbital_Properties"]
        self.simple_orbital_properties = settings_dict["Simple_Orbital_Properties"]
        self.specularReflection = settings_dict["Specular_Reflection"]
        self.opticalMaterial = settings_dict["Optical_Material"]
