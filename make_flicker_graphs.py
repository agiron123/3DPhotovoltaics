import Simulation
from Statistics import *
import matplotlib.pyplot as plt
import math

#recreating a few graphs from flickers paper on derivation of power gain
sim = []
theory = []
const = (2 * 40 * 40 * math.tan(math.pi / 4)) / (10 * (2 * 40 + 10))
settings = {}
settings["spacing"] = 10.0
settings["azimuth"] = 0.0
settings["zenith"] = math.pi / 4
settings["width"] = 40.0
settings["height"] = 40.0
for i in range(0, 95, 5):
    r = math.radians(i)
    print(r)
    settings["azimuth"] = r
    sim.append((i, Simulation.run(settings, Statistics())))
    theory.append((i, const*(math.cos(r) + math.sin(r)) + 1))

plt.plot([p[0] for p in sim], [p[1] for p in sim], label="simulation")
plt.plot([p[0] for p in theory], [p[1] for p in theory], label="theory")
plt.legend()
plt.xlabel("Azimuth (degrees)")
plt.ylabel("Avg # Interactions")
plt.title("Azimuth vs Avg interactions d=10, w=40, h=40")
plt.show()


settings = {}

settings["zenith"] = math.radians(85)
settings["azimuth"] = math.radians(35)
settings["width"] = 10.0
settings["spacing"] = 10.0
settings["height"] = 40.0

const = 2 * 40 * 10 * math.tan(math.radians(85)) * (math.cos(math.radians(35)) + math.sin(math.radians(35)))
sim = []
theory = []
for i in  [10, 100, 1000, 10000]:
    settings["spacing"] = i
    print("graphs", i)
    sim.append((math.log(i, 10), Simulation.run(settings, Statistics())))
    theory.append((math.log(i, 10), const / (i * (2 * 10 + i)) + 1))

plt.plot([p[0] for p in sim], [p[1] for p in sim], label="simulation")
plt.plot([p[0] for p in theory], [p[1] for p in theory], label="theory")
plt.legend()
plt.xlabel("log(spacing) micro meters")
plt.ylabel("Avg # Interactions")
plt.title("log(spacing) vs avg interactions d=10, w=4, zentih=85, azimuth=35")
plt.show()