"""Holds the Material class"""
import math
import random


class Material(object):
    """
    Represents the material that a tower is coated with.
    Is responsible for determining whether a photon is absorbed with the proper probability
    """
    """ @cvar hc: Planck's constant times speed of light (in electron volt nanometers)
        @type hc: floating point number
    """
    hc = 1239.84193  # Planck's constant times speed of light (in electron volt nanometers)
    def __init__(self, abs_coeff, band_gap):
        """
        Create a material with the given absorption coefficient and band gap
        @type abs_coeff: floating point number
        @param abs_coeff: The absorption coefficient of the material
        @type band_gap: floating point number
        @param band_gap: The bandgap of the material
        """
        self.abs_coeff = abs_coeff
        lambda_max = Material.hc / band_gap
        self.extinct_coeff = lambda_max * abs_coeff / (10000000.0 * 4.0 * math.pi)
        self.band_gap = band_gap

    #TODO : ported christians code from processing, need to confirm correctness
    def is_absorbed(self, photon):
        """
        Determine with the proper probability whether the photon is absorbed or not
        @type photon: Photon object
        @param photon: The photon which may be absorbed
        @rtype: boolean
        @return: boolean indicating whether the photon was absorbed or not
        """
        #TODO : The accuracy of this needs to be confimred, especially units, should probably check in with Ricardo
        if self.band_gap > Material.hc / photon.wavelength:
            return False
        alpha = 10000000.0 * 4.0 * math.pi * self.extinct_coeff / photon.wavelength  # alpha = 4*PI*k/lambda
        x = random.uniform(0.00001, 0.001)
        return random.random() < alpha * x