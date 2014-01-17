class Material(object):
    """Represents the material that a tower is coated with.
        Is responsible for determining whether a photon is absorbed with the proper probability"""
    def __init__(self,abs_coeff,bandgap):
        """Create a material with the given absorption coefficient and band gap"""
        self.abs_coeff=abs_coeff
        self.bandgap=bandgap

    def is_absorbed(self):
        """Determine with the proper probability whether the photon is absorbed or not"""
        return True

