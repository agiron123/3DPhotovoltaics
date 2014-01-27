class Material(object):
    """Represents the material that a tower is coated with.
        Is responsible for determining whether a photon is absorbed with the proper probability"""
    def __init__(self,abs_coeff,bandgap):
        """Create a material with the given absorption coefficient and band gap"""
        self.abs_coeff=abs_coeff
        self.bandgap=bandgap

    #TODO : bitch about photon being left out of is_absorbed method
    def is_absorbed(self, photon):
        """Determine with the proper probability whether the photon is absorbed or not"""
        #TODO : Implement me
        return True

    def reflect(self, photon, record):
        """Perform non-specular reflection of photon based upon record"""
        #TODO : Implement me
        raise Exception("Non-specular reflection has not been implemented yet.")