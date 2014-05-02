"""Contains the run method for running the simulation"""
from Orbit.SimpleOrbit import *
from Photon import *
from Data_Output.Stat import *
from Tower.Material import *
from Tower.Tower import *
import math


def run(settings, statistics):
    """
    Run the simulation using the given settings. Record the output to the given
    statistics object. Run receives a settings object from main, this contains all of the relevant information needed to set up
    and run the simulation.

    This run method is the principle coordinator of the simulation. It makes calls to other classes and methods as necessary
    but does all of the coordination and control flow in this method.

    @type settings: SimulationSettings Object
    @param settings: Holds all of the information used to configure the simulation in the correct form
    @type statistics: Statistics Object
    @param statistics: The Statistics object which will be used to record all of the data produced by the simulation

    """
    #setup the simulation using the data from the setting object
    i, photon_count, absorbing, trapping, = 0, settings.fixed_orbit['photon_count'], settings.absorbing, settings.trapping
    specular_only = not settings.non_specular_reflection
    ignore_tower_tops = not settings.tower_tops
    orbit = SimpleOrbit(1, settings.fixed_orbit['zenith_angle'], settings.fixed_orbit['azimuth_angle'])
    photon = Photon(0, 0, 0, 0, 0)
    #set up the material
    material = Material(settings.material_profile["absorption_coefficient"], settings.material_profile["band_gap"])
    tower = Tower(settings.tower["height"], material, settings.tower["pitch"], settings.tower["width"], settings.tower["shape"])

    #TODO: this terminating condition will need to be changed when we incoporate orbit
    while i < photon_count:
        #generate a new photon from orbit
        photon = orbit.generate_photon(photon, tower)
        #generate new stat datum
        stat = Stat(photon)
        done = False
        if tower.is_inside(photon):
            if not ignore_tower_tops:
                done = True
                record = Record(False, 0, photon.position, np.array([0, 0, 1]), True)
                if absorbing and tower.material.is_absorbed(photon):
                    stat.absorb(photon, record)
                elif trapping and photon.is_trapped():
                    stat.trap(photon, record)
                else:
                    stat.reflect(photon, record)
            else:
                #completely ignore photons spawned on the top of the tower
                continue
        #continue until photon is absorbed, trapped, or exits the simulation
        while not done:
            #get a collision
            record = tower.get_record(photon)
            #check 3 things
            #exiting
            if record.is_exiting:
                stat.exit(photon)
                done = True  # move onto next photon
            #wrap around
            elif record.is_boundary:
                stat.wrap_around(photon, record)
                photon.wrap_around(record)
            #absorbed
            elif absorbing and tower.material.is_absorbed(photon):
                stat.absorb(photon, record)
                done = True  # move onto next photon
            #trapped
            elif trapping and photon.trapped(record):
                #TODO : do trapping work here
                stat.trap(photon, record)
                #something else?
                done = True  # move onto next photon
            elif specular_only:
                photon.specular_reflect(record)
                stat.reflect(photon, record)
            else:
                photon.non_specular_reflect(record)
        #finish with this photon by updating statistics with its stat datum
        statistics.update(stat)
        i += 1