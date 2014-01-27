
class Orbit(object):
    """Represents the orbit of the ISS in space.
        Is responsible for generating an accurate probability distribution
        of intial photon parameters (e.g. velocity, wavelength, etc.). Is also responsible for
        determining how many photons will be fired per time step."""

    def __init__(self):
        """Initialize the orbit given the initial parameters"""
        #not sure what exactly to put here right now, we need a better understanding of the physics
        #to determine that exactly, beta angles, and earth shine definitely seem like things which should go here

    def generate_photon(self, photon, tower):
        """Reset the photon which the simulation is using to represent a new photon"""
        #TODO : hard physics stuff goes here
        #NOTE : leaving a normal distribution here


    def time_step(self, delta_t):
        """Move the ISS along the orbit by the given time step. The probability distribution of
            generate_photon will reflect this change"""