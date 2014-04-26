"""Contains class for an orbit that models the ISS orbiting the earth"""
__author__ = 'cxaviousb'
from Orbit import *

from sgp4.earth_gravity import wgs72
import sgp4.propagation


class SimpleOrbit(Orbit):
    """Orbit class for simulating solar radiation hitting a solar cell orbiting the Earth on the ISS nadir.
    This model excludes the effect of gravity on solar radiation's trajectory.
    This model excludes !partial! blocking of solar radiation due to Earth and/or parts of the ISS itself.

    Capabilities include the following:
    0 Orbit of the ISS around the Earth
    O Relative orientation of the ISS to the Earth during orbit
    O Relative orientation of the solar to the ISS
    O Calculation of coordinate space source of solar radiation
    O Conversion of solar radiation to the solar cell's frame of reference

    PS O indicates feature unimplemented.
       0 indicates feature is partially implemented.
       x indicates feature is fully implemented.
       X indicates feature is fully implemented and has been tested for accuracy."""
    def __init__(self, tle, tstart, tend):
        """Create a simple orbit using the given spherical coordinates"""
        self.whichconst = wgs72
        self.tstart = tstart
        self.tsince = tstart
        self.tend = tend
        self.tle = tle

        if not tle.line1.startswith('1'):
            raise Exception("Invalid TLE: Line 1 of two-line element does not start with '1'.")
        if not tle.line2.startswith('2'):
            raise Exception("Invalid TLE: Line 2 of two-line element does not start with '2'.")

        self.satrec = sgp4.propagation.twoline2rv(self.tle.line1, self.tle.line2, self.whichconst)
        self.sat_pos, self.sat_vel = sgp4.propagation.sgp4(self.satrec, self.tstart)
        if self.sat_pos is None:
            raise Exception("Error in Brandon Rhode's sgp4 model: satellite position return was 'None'.")

        self.mu = self.satrec.whichconst.mu

    def generate_photon(self, photon, tower):
        """Return a photon with correct initial velocity, position and wavelength for solar radiation originating from
        the sun."""
        raise Exception("OrbitWithSunshine's generate_photon method is unimplemented.")
        return None

    def step_time(self, delta):
        """Update the positions of the sun, ISS, and Earth relative to one another."""

        """Updates position of ISS relative to the Earth"""
        self.tsince += delta
        self.sat_pos, self.sat_vel = sgp4.propagation.sgp4(self.satrec, self.tsince)
        if self.sat_pos is None:
            raise Exception("Error in Brandon Rhode's sgp4 model: satellite position return was 'None'.")

    def is_orbit_complete(self):
        """Return boolean of whether or not current time in orbit has passed user defined end of orbit."""
        return self.tsince > self.tend