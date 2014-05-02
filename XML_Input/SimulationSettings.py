"""Holds the SimulationSettings class"""
import math
class SimulationSettings(object):
    """
    Class to hold the SimulationSettings that were parsed from the XML file.
    """

    def __init__(self, d):
        """
        Create the simulation settings object using the given dictionary.
        The dictionary is passed from the XML parser.
        @type d: dictionary
        @param d: dictionary containing all the info needed for initialization
        """
        self.panel_settings = d["panel_settings"]
        self.material_profile = d["material_profile"]
        self.tower = d["tower"]
        if 'fixed_orbit' in d['orbital_properties']:
            self.fixed_orbit = d['orbital_properties']['fixed_orbit']
            #all angle in the code use radians so we do the conversion here
            #from here out all angles are in radians
            self.fixed_orbit['zenith_angle'] = math.radians(self.fixed_orbit['zenith_angle'])
            self.fixed_orbit['azimuth_angle'] = math.radians(self.fixed_orbit['azimuth_angle'])
        else:
            self.real_orbit = d['real_orbit']
        self.non_specular_reflection = d["non_specular_reflection"]
        self.optical_material = d["optical_material"]
        self.trapping = d["trapping"]
        #If false photons spawning over tower tops are ignored
        self.tower_tops = d["tower_tops"]
        self.absorbing = d["absorbing"]
