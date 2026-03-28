"""
In this experiment, we showcase the collision mechanic of our simulation.
The collision is modeled as a repulsive force that activates when particles overlap.

Observations:
When particles collide, the repulsive force pushes them apart. However, because 
it is a force-based approximation rather than an instantaneous state change, 
particles may slightly overlap before changing direction. 

If the collision factor 'k' is too small, particles might pass through each other. 
The efficiency of 'k' depends on the particle radius and their velocities.
"""

from view import *
from model import Vec, Particle, collision, wall_collision # Importera från model.py
import math

# 1. Skapa partiklar i ett cirkulärt mönster som rör sig inåt mot mitten
n = 7
particles = []
for i in range(n):
    theta = i * 2 * math.pi / n
    u = Vec(math.cos(theta), math.sin(theta))
    pos = 5 * u
    vel = -10 * u 
    particles.append(Particle(1, pos, vel, 1))

# 2. Skapa väggar (för att hålla partiklarna på skärmen efter kollisionen)
walls(canvas, particles[0].radius) 

# 3. Definiera konstanter
K_FACTOR = 500
TIME_STEP = 0.0001

# 4. STARTA SIMULERINGEN
# Vi skickar in en lambda som kör collision() följt av vägg-logiken.
# Detta följer instruktionen att inte definiera nya metoder i experimentfilen.
simulation_loop(
    lambda dt, pts: (
        collision(dt, pts, K_FACTOR),
        wall_collision(pts, Vec(-1, 0), Vec(8, 0)),
        wall_collision(pts, Vec(1, 0), Vec(-8, 0)),
        wall_collision(pts, Vec(0, -1), Vec(0, 8)),
        wall_collision(pts, Vec(0, 1), Vec(0, -8))
    ), 
    TIME_STEP, 
    particles
)