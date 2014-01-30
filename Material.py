import math
import random


class Material(object):
    """Represents the material that a tower is coated with.
        Is responsible for determining whether a photon is absorbed with the proper probability"""
    hc = 1239.84193  # Planck's constant times speed of light (in electron volt nanometers)
    def __init__(self, abs_coeff, band_gap):
        """Create a material with the given absorption coefficient and band gap"""
        self.abs_coeff = abs_coeff
        lambda_max = Material.hc / band_gap
        self.extinct_coeff = lambda_max * abs_coeff / (10000000.0 * 4.0 * math.PI)
        self.band_gap = band_gap

    #TODO : ported christians code from processing, need to confirm correctness
    def is_absorbed(self, photon):
        """Determine with the proper probability whether the photon is absorbed or not"""
        #TODO : The accuracy of this needs to be confimred, especially units, should probably check in with Ricardo
        if self.band_gap > Material.hc / photon.wavelength:
            return False
        alpha = 10000000.0 * 4.0 * math.PI * self.extinct_coeff / photon.wavelength  # alpha = 4*PI*k/lambda
        x = random.uniform(0.0001, 0.01)
        return random.uniform(1.0) > alpha * x