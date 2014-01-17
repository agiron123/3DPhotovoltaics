import numpy as np
import Stat

class Photon(object):
    """Represents a photon in the simulation. Only one photon is ever made, it is just reset when needed"""
    def __init__(self,position,velocity,wavelength,):
        self.position=position
        self.velocity=velocity
        self.wavelength=wavelength
        self.stat=Stat()

    #leaving this here for now but we don't really need it
    #orbit can just do the resetting
    def reset(self,position,velocity,wavelength):
        """Avoid the costs associated with creating and destroying objects by just reseting the photon
                instead of making a new one"""
        self.position=position
        self.velocity=velocity
        self.wavelength=wavelength