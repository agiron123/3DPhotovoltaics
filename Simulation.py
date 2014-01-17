import Orbit
import Tower
import Photon
import Record

def run(arguments,statistics):
    """Run recieves an arguments dictionary from main, this contains all of the relevant information needed to setup
    and run the simulation in the form of key value pairs"""
    #pass relevant arguments to each of these constructor functions, details omitted for now
    orbit=Orbit()
    tower=Tower()
    photon=Photon()
    t,total_time=0,10**6
    #outer most loop, we either need to run the simulation for some amount of time
    #or for some distance of orbit, something like that
    while t<total_time:
        #now given that the ISS is in one fixed position we need to "fire" some number of photons at it
        #this number will probably vary based on the position in the orbit, the orbit class will need to store this
        photon_count=0
        while photon_count<orbit.total:
            #give orbit the photon to update it
            orbit.generate_photon(photon)
            #check if the photon is outside a tower, not enough going on yet to write this
            record=Record()
            while record != None:
                record=tower.get_record(photon)
                #check 3 things
                #-exiting, - absorbed, - trapped
                #update the stat here
                #update the photon here, reflect it
                statistics.update(photon.stat)
        #move the ISS in the orbit, update by a time step
        orbit.time_step(10)
        t+=10

