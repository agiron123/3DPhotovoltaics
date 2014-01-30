import math
import random
class Material(object):
    """Represents the material that a tower is coated with.
        Is responsible for determining whether a photon is absorbed with the proper probability"""
    hc = 1239.84193; #Planck's constant times speed of light (in electron volt nanometers)
    def __init__(self,abs_coeff,bandgap):
        """Create a material with the given absorption coefficient and band gap"""
        self.abs_coeff=abs_coeff
        self.bandgap=bandgap

    #TODO : ported christians code from processing, need to confirm correctness
    def is_absorbed(self, photon):
        """Determine with the proper probability whether the photon is absorbed or not"""
        #TODO : Implement me
        if self.bandgap> Material.hc/photon.wavelength:
            return False
        alpha = 10000000.0*4.0*math.pi*0.00658/photon.wavelength #alpha = 4*PI*k/lambda;
        x = random.uniform(0.0001, 0.01)
        if random.random() > alpha*x:
            return True
        else:
            return False

    def reflect(self, photon, record):
        """Perform non-specular reflection of photon based upon record"""
        #TODO : Implement me
        raise Exception("Non-specular reflection has not been implemented yet.")