import Simulation
from SimulationSettings import *
from Statistics import *
import matplotlib.pyplot as plt
import math

#recreating a few graphs from flickers paper on derivation of power gain
#rect prism
def vary_azimuth():
    #rect prism
    sim = []
    theory = []
    const = (2 * 40 * 40 * math.tan(math.pi / 4)) / (10 * (2 * 40 + 10))
    settings = {}
    settings["Tower"] = {}
    settings["Tower"]["pitch"] = 10.0
    settings["Simple_Orbital_Properties"] = {}
    settings["Simple_Orbital_Properties"]["azumithal_angle"] = 0.0
    settings["Simple_Orbital_Properties"]["zenith_angle"] = math.pi / 4
    settings["Tower"]["width"] = 40.0
    settings["Tower"]["height"] = 40.0
    settings["Tower"]["shape"] = "rect_prism"
    settings["Specular_Reflection"] = True
    #not used in these basic test
    settings["Material_profile"] = {}
    settings["Material_profile"]["absorption_coefficient"] = 1
    settings["Material_profile"]["band_gap"] = 1
    settings["Orbital_Properties"] = None
    settings["Optical_Material"] = None
    for i in range(0, 95, 5):
        r = math.radians(i)
        print(r)
        settings["Simple_Orbital_Properties"]["azumithal_angle"] = r
        sim.append((i, Simulation.run(SimulationSettings(settings), Statistics())))
        theory.append((i, const*(math.cos(r) + math.sin(r)) + 1))
    plt.subplot(3, 1, 1)
    plt.plot([p[0] for p in sim], [p[1] for p in sim], label="simulation")
    plt.plot([p[0] for p in theory], [p[1] for p in theory], label="theory")
    plt.legend()
    plt.xlabel("Azimuth (degrees)")
    plt.ylabel("Avg # Interactions")
    plt.title("Rectangular Prism d=10, w=40, h=40")



    #xtrench
    sim = []
    theory = []
    const = (2 * 40 * math.tan(math.pi / 4)) / 10
    settings = {}
    settings["Tower"] = {}
    settings["Tower"]["pitch"] = 10.0
    settings["Simple_Orbital_Properties"] = {}
    settings["Simple_Orbital_Properties"]["azumithal_angle"] = 0.0
    settings["Simple_Orbital_Properties"]["zenith_angle"] = math.pi / 4
    settings["Tower"]["width"] = 40.0
    settings["Tower"]["height"] = 40.0
    settings["Tower"]["shape"] = "xtrench"
    settings["Specular_Reflection"] = True
    #not used in these basic test
    settings["Material_profile"] = {}
    settings["Material_profile"]["absorption_coefficient"] = 1
    settings["Material_profile"]["band_gap"] = 1
    settings["Orbital_Properties"] = None
    settings["Optical_Material"] = None
    for i in range(0, 95, 5):
        r = math.radians(i)
        print(r)
        settings["Simple_Orbital_Properties"]["azumithal_angle"] = r
        sim.append((i, Simulation.run(SimulationSettings(settings), Statistics())))
        theory.append((i, const*(math.cos(r)) + 1))
    plt.subplot(3, 1, 2)
    plt.plot([p[0] for p in sim], [p[1] for p in sim], label="simulation")
    plt.plot([p[0] for p in theory], [p[1] for p in theory], label="theory")
    plt.legend()
    plt.xlabel("Azimuth (degrees)")
    plt.ylabel("Avg # Interactions")
    plt.title("X-Trench d=10, w=40, h=40")
    #box sim
    sim = []
    theory = []
    const = (2 * 40 * math.tan(math.pi / 4)) / 10
    settings = {}
    settings["Tower"] = {}
    settings["Tower"]["pitch"] = 10.0
    settings["Simple_Orbital_Properties"] = {}
    settings["Simple_Orbital_Properties"]["azumithal_angle"] = 0.0
    settings["Simple_Orbital_Properties"]["zenith_angle"] = math.pi / 4
    settings["Tower"]["width"] = 40.0
    settings["Tower"]["height"] = 40.0
    settings["Tower"]["shape"] = "box"
    settings["Specular_Reflection"] = True
    #not used in these basic test
    settings["Material_profile"] = {}
    settings["Material_profile"]["absorption_coefficient"] = 1
    settings["Material_profile"]["band_gap"] = 1
    settings["Orbital_Properties"] = None
    settings["Optical_Material"] = None
    for i in range(0, 95, 5):
        r = math.radians(i)
        print(r)
        settings["Simple_Orbital_Properties"]["azumithal_angle"] = r
        sim.append((i, Simulation.run(SimulationSettings(settings), Statistics())))
        theory.append((i, const*(math.cos(r) + math.sin(r)) + 1))
    plt.subplot(3, 1, 3)
    plt.plot([p[0] for p in sim], [p[1] for p in sim], label="simulation")
    plt.plot([p[0] for p in theory], [p[1] for p in theory], label="theory")
    plt.legend()
    plt.xlabel("Azimuth (degrees)")
    plt.ylabel("Avg # Interactions")
    plt.title("Box d=10, w=40, h=40")
    plt.tight_layout()
    plt.show()

def vary_height():
    #rect prism
    sim = []
    theory = []
    const = (2 * 4 * math.tan(math.radians(85))) / (10 * (2 * 4 + 10)) * (math.cos(math.radians(35)) + math.sin(math.radians(35)))
    settings = {}
    settings["Tower"] = {}
    settings["Tower"]["pitch"] = 10.0
    settings["Simple_Orbital_Properties"] = {}
    settings["Simple_Orbital_Properties"]["azumithal_angle"] = math.radians(35)
    settings["Simple_Orbital_Properties"]["zenith_angle"] = math.radians(85)
    settings["Tower"]["width"] = 4
    settings["Tower"]["height"] = 10
    settings["Tower"]["shape"] = "rect_prism"
    settings["Specular_Reflection"] = True
    #not used in these basic test
    settings["Material_profile"] = {}
    settings["Material_profile"]["absorption_coefficient"] = 1
    settings["Material_profile"]["band_gap"] = 1
    settings["Orbital_Properties"] = None
    settings["Optical_Material"] = None
    for i in range(500, 4000, 500):
        print(i)
        settings["Tower"]["height"] = i
        x = Simulation.run(SimulationSettings(settings), Statistics())
        print(x)
        sim.append((i, x))
        theory.append((i, const * i + 1))
    plt.subplot(3, 1, 1)
    plt.plot([p[0] for p in sim], [p[1] for p in sim], label="simulation")
    plt.plot([p[0] for p in theory], [p[1] for p in theory], label="theory")
    plt.legend()
    plt.xlabel("Height (micro meters)")
    plt.ylabel("Avg # Interactions")
    plt.title("Rectangular Prism d=10, w=4, zenith=85, azimuth=35")
    plt.show()
"""
    #xtrench
    sim = []
    theory = []
    const = (2 * math.tan(math.pi / 4) * math.sin(math.radians(35))) / 10
    settings = {}
    settings["Tower"] = {}
    settings["Tower"]["pitch"] = 10.0
    settings["Simple_Orbital_Properties"] = {}
    settings["Simple_Orbital_Properties"]["azumithal_angle"] = math.radians(35)
    settings["Simple_Orbital_Properties"]["zenith_angle"] = math.pi / 4
    settings["Tower"]["width"] = 4
    settings["Tower"]["height"] = 10
    settings["Tower"]["shape"] = "rect_prism"
    settings["Specular_Reflection"] = True
    #not used in these basic test
    settings["Material_profile"] = {}
    settings["Material_profile"]["absorption_coefficient"] = 1
    settings["Material_profile"]["band_gap"] = 1
    settings["Orbital_Properties"] = None
    settings["Optical_Material"] = None
    for i in range(500, 4000, 500):
        print(i)
        settings["Tower"]["height"] = i
        sim.append((i, Simulation.run(SimulationSettings(settings), Statistics())))
        theory.append((i, const * i + 1))
    plt.subplot(3, 1, 1)
    plt.plot([p[0] for p in sim], [p[1] for p in sim], label="simulation")
    plt.plot([p[0] for p in theory], [p[1] for p in theory], label="theory")
    plt.legend()
    plt.xlabel("Height (micro meters)")
    plt.ylabel("Avg # Interactions")
    plt.title("X-Trench d=10, w=4, zenith=85, azimuth=35")

    #box sim
    sim = []
    theory = []
    const = (2 * 40 * math.tan(math.pi / 4)) / 10
    settings = {}
    settings["Tower"] = {}
    settings["Tower"]["pitch"] = 10.0
    settings["Simple_Orbital_Properties"] = {}
    settings["Simple_Orbital_Properties"]["azumithal_angle"] = 0.0
    settings["Simple_Orbital_Properties"]["zenith_angle"] = math.pi / 4
    settings["Tower"]["width"] = 40.0
    settings["Tower"]["height"] = 40.0
    settings["Tower"]["shape"] = "box"
    settings["Specular_Reflection"] = True
    #not used in these basic test
    settings["Material_profile"] = {}
    settings["Material_profile"]["absorption_coefficient"] = 1
    settings["Material_profile"]["band_gap"] = 1
    settings["Orbital_Properties"] = None
    settings["Optical_Material"] = None
    for i in range(0, 95, 5):
        r = math.radians(i)
        print(r)
        settings["Simple_Orbital_Properties"]["azumithal_angle"] = r
        sim.append((i, Simulation.run(SimulationSettings(settings), Statistics())))
        theory.append((i, const*(math.cos(r) + math.sin(r)) + 1))
    plt.subplot(3, 1, 3)
    plt.plot([p[0] for p in sim], [p[1] for p in sim], label="simulation")
    plt.plot([p[0] for p in theory], [p[1] for p in theory], label="theory")
    plt.legend()
    plt.xlabel("Azimuth (degrees)")
    plt.ylabel("Avg # Interactions")
    plt.title("Box d=10, w=40, h=40")
    plt.tight_layout()
    plt.show()
    """

vary_height()