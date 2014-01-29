import Orbit
import Tower
import Photon
import Record

def run(settings,statistics):
    """Run receives an arguments dictionary from main, this contains all of the relevant information needed to setup
    and run the simulation in the form of key value pairs"""
    #pass relevant arguments to each of these constructor functions, details omitted for now
    #TODO : un-omit details
    orbit = Orbit()
    tower = Tower()
    #TODO : determine what time scale we will use throughout the program
    t, total_time, delta_t = 0, 10**6, 10
    #outer most loop, we either need to run the simulation for some amount of time
    #or for some distance of orbit, something like that
    while t < total_time:
        #now given that the ISS is in one fixed position we need to "fire" some number of photons at it
        #this number will probably vary based on the position in the orbit, the orbit class will need to store this
        photon_count = 0
        while photon_count < settings.photonsPerPoint:
            #generate a new photon from orbit
            photon = orbit.generate_photon()
            #generate new stat datum
            stat = Stat(photon)
            #check if the photon is outside a tower, not enough going on yet to write this
            if tower.contains(photon):
                #TODO : handle photon being spawned at the top of tower
                raise ValueError
                continue
            record = tower.get_record(photon)
            while record is not None:
                #check 3 things
                #-exiting
                if record.time == float('inf'):
                    #TODO : do exiting work
                    stat.exit(photon)
                    break  # move onto next photon
                #-wrap around
                if record.material is None:
                    #TODO : do wrap around work
                    stat.wrap_around(photon, record)
                    #update photon to other side of cell
                    record = tower.get_record(photon)  # move onto next collision
                    continue
                #-absorbed
                if settings.absorbing and record.material.is_absorbed(photn):
                    stat.absorb(photon, record)
                    break  # move onto next photon
                #-trapped
                if settings.trapping and record.material.trapped(photon):
                    #TODO : do trapping work here
                    stat.trap(photon, record)
                    #something else?
                    break  # move onto next photon
                if settings.specularOnly:
                    photon.reflect(record.normal)
                else:
                    material.reflect(photon)
                #move onto next collision
                record = tower.get_record(photon)
            #finish with this photon by updating statistics with its stat datum
            statistics.update(stat)
        #move the ISS in the orbit, update by a time step
        #TODO : determine if delta_t needs to be translated to radians and how to do so
        orbit.time_step(delta_t)
        t += delta_t

