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
    maxerror = 0
    for i in range(0, 95, 5):
        r = math.radians(i)
        print(r)
        settings["Simple_Orbital_Properties"]["azumithal_angle"] = r
        x = Simulation.run(SimulationSettings(settings), Statistics())
        y = const*(math.cos(r) + math.sin(r)) + 1
        sim.append((i, x))
        theory.append((i, y))
        error = math.fabs(x-y) / y * 100
        if error > maxerror:
            maxerror = error
    print("rect prism max error", maxerror)
    plt.subplot(3, 1, 1)
    plt.plot([p[0] for p in sim], [p[1] for p in sim], 'bo', label="simulation")
    plt.plot([p[0] for p in theory], [p[1] for p in theory], 'r', label="theory")
    plt.legend()
    plt.xlabel("Azimuth (degrees)")
    plt.ylabel("Avg # Interactions")
    plt.title("Rectangular Prism d=10, w=40, h=40, zenith=45")


    maxerror = 0
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
        x = Simulation.run(SimulationSettings(settings), Statistics())
        y = const*(math.cos(r)) + 1
        sim.append((i, x))
        theory.append((i, y))
        if error > maxerror:
            maxerror = error
    print("xtrench max error", maxerror)
    plt.subplot(3, 1, 2)
    plt.plot([p[0] for p in sim], [p[1] for p in sim], 'bo', label="simulation")
    plt.plot([p[0] for p in theory], [p[1] for p in theory], 'r', label="theory")
    plt.legend()
    plt.xlabel("Azimuth (degrees)")
    plt.ylabel("Avg # Interactions")
    plt.title("X-Trench d=10, w=40, h=40, zenith=45")
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
        x = Simulation.run(SimulationSettings(settings), Statistics())
        y = const*(math.cos(r) + math.sin(r)) + 1
        sim.append((i, x))
        theory.append((i, y))
        error = math.fabs(x-y) / y * 100
        if error > maxerror:
            maxerror = error
    print("box Max error", maxerror)
    plt.subplot(3, 1, 3)
    plt.plot([p[0] for p in sim], [p[1] for p in sim], 'bo', label="simulation")
    plt.plot([p[0] for p in theory], [p[1] for p in theory], 'r', label="theory")
    plt.legend()
    plt.xlabel("Azimuth (degrees)")
    plt.ylabel("Avg # Interactions")
    plt.title("Box d=10, w=40, h=40, zenith=45")
    plt.tight_layout()
    plt.show()


def vary_height():
    """
    #rect prism
    sim = []
    theory = []
    const = (2 * 4 * math.tan(math.radians(85))) / (10 * (2 * 4 + 10)) * (math.cos(math.radians(35)) + math.sin(math.radians(35)))
    print(const)
    settings = {}
    settings["Tower"] = {}
    settings["Tower"]["pitch"] = 10.0
    settings["Simple_Orbital_Properties"] = {}
    settings["Simple_Orbital_Properties"]["azumithal_angle"] = math.radians(35)
    settings["Simple_Orbital_Properties"]["zenith_angle"] = math.radians(85)
    settings["Tower"]["width"] = 4.0
    settings["Tower"]["height"] = 10.0
    settings["Tower"]["shape"] = "rect_prism"
    settings["Specular_Reflection"] = True
    #not used in these basic test
    settings["Material_profile"] = {}
    settings["Material_profile"]["absorption_coefficient"] = 1
    settings["Material_profile"]["band_gap"] = 1
    settings["Orbital_Properties"] = None
    settings["Optical_Material"] = None
    maxerror = 0
    for i in range(500, 4000, 500):
        settings["Tower"]["height"] = i / 1.0
        x = Simulation.run(SimulationSettings(settings), Statistics())
        y = const * i + 1
        sim.append((i, x))
        theory.append((i, y))
        print(i, x, y)
        error = math.fabs(x-y) / y * 100
        if error > maxerror:
            maxerror = error
    print("max error rect prism", maxerror)
    plt.subplot(3, 1, 1)
    plt.plot([p[0] for p in sim], [p[1] for p in sim], 'bo', label="simulation")
    plt.plot([p[0] for p in theory], [p[1] for p in theory], 'r', label="theory")
    plt.xlabel("Height (micro meters)")
    plt.ylabel("Avg # Interactions")
    plt.title("Rectangular Prism d=10, w=4, zenith=85, azimuth=35")
    #xtrench
    maxerror = 0
    sim = []
    theory = []
    const = (2 * math.tan(math.radians(85)) * math.cos(math.radians(35))) / 10
    settings = {}
    settings["Tower"] = {}
    settings["Tower"]["pitch"] = 10.0
    settings["Simple_Orbital_Properties"] = {}
    settings["Simple_Orbital_Properties"]["azumithal_angle"] = math.radians(35)
    settings["Simple_Orbital_Properties"]["zenith_angle"] = math.radians(85)
    settings["Tower"]["width"] = 4.0
    settings["Tower"]["height"] = 10.0
    settings["Tower"]["shape"] = "xtrench"
    settings["Specular_Reflection"] = True
    #not used in these basic test
    settings["Material_profile"] = {}
    settings["Material_profile"]["absorption_coefficient"] = 1
    settings["Material_profile"]["band_gap"] = 1
    settings["Orbital_Properties"] = None
    settings["Optical_Material"] = None
    for i in range(500, 4000, 500):
        print(i)
        settings["Tower"]["height"] = i / 1.0
        x = Simulation.run(SimulationSettings(settings), Statistics())
        y = const * i + 1
        sim.append((i, x))
        theory.append((i, y))
        print(i, x, y)
        error = math.fabs(x-y) / y * 100
        if error > maxerror:
            maxerror = error
    print("xtrench max error", maxerror)
    plt.subplot(3, 1, 2)
    plt.plot([p[0] for p in sim], [p[1] for p in sim], 'bo', label="simulation")
    plt.plot([p[0] for p in theory], [p[1] for p in theory], 'r', label="theory")
    plt.xlabel("Height (micro meters)")
    plt.ylabel("Avg # Interactions")
    plt.title("X-Trench d=10, w=4, zenith=85, azimuth=35")
"""
    #box sim
    maxerror = 0
    sim = []
    theory = []
    const = (2 * math.tan(math.radians(85)) / 10) * (math.cos(math.radians(35)) + math.sin(math.radians(35)))
    settings = {}
    settings["Tower"] = {}
    settings["Tower"]["pitch"] = 10.0
    settings["Simple_Orbital_Properties"] = {}
    settings["Simple_Orbital_Properties"]["azumithal_angle"] = math.radians(35)
    settings["Simple_Orbital_Properties"]["zenith_angle"] = math.radians(85)
    settings["Tower"]["width"] = 4.0
    settings["Tower"]["height"] = 0.0
    settings["Tower"]["shape"] = "box"
    settings["Specular_Reflection"] = True
    #not used in these basic test
    settings["Material_profile"] = {}
    settings["Material_profile"]["absorption_coefficient"] = 1
    settings["Material_profile"]["band_gap"] = 1
    settings["Orbital_Properties"] = None
    settings["Optical_Material"] = None
    for i in range(500, 4000, 500):
        print(i)
        settings["Tower"]["height"] = i / 1.0
        x = Simulation.run(SimulationSettings(settings), Statistics())
        y = const * i + 1
        sim.append((i, x))
        theory.append((i, y))
        print(i, x, y)
        error = math.fabs(x-y) / y * 100
        if error > maxerror:
            maxerror = error
    print("box max error is", maxerror)
    plt.subplot(3, 1, 3)
    plt.plot([p[0] for p in sim], [p[1] for p in sim], 'bo', label="simulation")
    plt.plot([p[0] for p in theory], [p[1] for p in theory], 'r', label="theory")
    plt.xlabel("Azimuth (degrees)")
    plt.ylabel("Avg # Interactions")
    plt.title("Box d=10, w=4, zenith=85, azimuth=35")
    plt.tight_layout()
    plt.show()


def vary_spacing():
    #rect prism
    sim = []
    theory = []
    const = (2 * 10 * 40 * math.tan(math.radians(85))) * (math.cos(math.radians(35)) + math.sin(math.radians(35)))
    settings = {}
    settings["Tower"] = {}
    settings["Tower"]["pitch"] = 10.0
    settings["Simple_Orbital_Properties"] = {}
    settings["Simple_Orbital_Properties"]["azumithal_angle"] = math.radians(35)
    settings["Simple_Orbital_Properties"]["zenith_angle"] = math.radians(85)
    settings["Tower"]["width"] = 10.0
    settings["Tower"]["height"] = 40.0
    settings["Tower"]["shape"] = "rect_prism"
    settings["Specular_Reflection"] = True
    #not used in these basic test
    settings["Material_profile"] = {}
    settings["Material_profile"]["absorption_coefficient"] = 1
    settings["Material_profile"]["band_gap"] = 1
    settings["Orbital_Properties"] = None
    settings["Optical_Material"] = None
    maxerror = 0
    for i in [1, 10, 100, 1000, 10000]:
        settings["Tower"]["pitch"] = i / 1.0
        x = Simulation.run(SimulationSettings(settings), Statistics())
        y = const / (i * (2 * 10 + i)) + 1
        sim.append((i, x))
        theory.append((i, y))
        print(i, x, y)
        error = math.fabs(x-y) / y * 100
        if error > maxerror:
            maxerror = error
    print("max error rect prism", maxerror)
    plt.subplot(3, 1, 1)
    plt.plot([math.log(p[0], 10) for p in sim], [p[1] for p in sim], 'bo', label="simulation")
    plt.plot([math.log(p[0], 10) for p in theory], [p[1] for p in theory], 'r', label="theory")
    plt.xlabel("log(d) micro meters")
    plt.ylabel("Avg # Interactions")
    plt.title("Rectangular Prism d=10, w=4, zenith=85, azimuth=35")
    #xtrench
    maxerror = 0
    sim = []
    theory = []
    const = (2 * 40 * math.tan(math.radians(85)) * math.cos(math.radians(35)))
    settings = {}
    settings["Tower"] = {}
    settings["Tower"]["pitch"] = 10.0
    settings["Simple_Orbital_Properties"] = {}
    settings["Simple_Orbital_Properties"]["azumithal_angle"] = math.radians(35)
    settings["Simple_Orbital_Properties"]["zenith_angle"] = math.radians(85)
    settings["Tower"]["width"] = 10.0
    settings["Tower"]["height"] = 40.0
    settings["Tower"]["shape"] = "xtrench"
    settings["Specular_Reflection"] = True
    #not used in these basic test
    settings["Material_profile"] = {}
    settings["Material_profile"]["absorption_coefficient"] = 1
    settings["Material_profile"]["band_gap"] = 1
    settings["Orbital_Properties"] = None
    settings["Optical_Material"] = None
    for i in [1, 10, 100, 1000, 10000]:
        print(i)
        settings["Tower"]["pitch"] = i / 1.0
        x = Simulation.run(SimulationSettings(settings), Statistics())
        y = const / i + 1
        sim.append((i, x))
        theory.append((i, y))
        print(i, x, y)
        error = math.fabs(x-y) / y * 100
        if error > maxerror:
            maxerror = error
    print("xtrench max error", maxerror)
    plt.subplot(3, 1, 2)
    plt.plot([math.log(p[0], 10) for p in sim], [p[1] for p in sim], 'bo', label="simulation")
    plt.plot([math.log(p[0], 10) for p in theory], [p[1] for p in theory], 'r', label="theory")
    plt.xlabel("log(d) micro meters")
    plt.ylabel("Avg # Interactions")
    plt.title("X-Trench w=10, h=40, zenith=85, azimuth=35")
    #box sim
    maxerror = 0
    sim = []
    theory = []
    const = (2 * 40 * math.tan(math.radians(85))) * (math.cos(math.radians(35)) + math.sin(math.radians(35)))
    settings = {}
    settings["Tower"] = {}
    settings["Tower"]["pitch"] = 10.0
    settings["Simple_Orbital_Properties"] = {}
    settings["Simple_Orbital_Properties"]["azumithal_angle"] = math.radians(35)
    settings["Simple_Orbital_Properties"]["zenith_angle"] = math.radians(85)
    settings["Tower"]["width"] = 10.0
    settings["Tower"]["height"] = 40.0
    settings["Tower"]["shape"] = "box"
    settings["Specular_Reflection"] = True
    #not used in these basic test
    settings["Material_profile"] = {}
    settings["Material_profile"]["absorption_coefficient"] = 1
    settings["Material_profile"]["band_gap"] = 1
    settings["Orbital_Properties"] = None
    settings["Optical_Material"] = None
    for i in [10, 10, 100, 1000, 10000]:
        print(i)
        settings["Tower"]["pitch"] = i / 1.0
        x = Simulation.run(SimulationSettings(settings), Statistics())
        y = const / i + 1
        sim.append((i, x))
        theory.append((i, y))
        print(i, x, y)
        error = math.fabs(x-y) / y * 100
        if error > maxerror:
            maxerror = error
    print("box max error is", maxerror)
    plt.subplot(3, 1, 3)
    plt.plot([math.log(p[0], 10) for p in sim], [p[1] for p in sim], 'bo', label="simulation")
    plt.plot([math.log(p[0], 10) for p in theory], [p[1] for p in theory], 'r', label="theory")
    plt.xlabel("log(d) micro meters")
    plt.ylabel("Avg # Interactions")
    plt.title("Box w=10, h=40, zenith=85, azimuth=35")
    plt.tight_layout()
    plt.show()

vary_spacing()