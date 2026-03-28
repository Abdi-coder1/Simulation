"""
In this experiment, we showcase the gravitational force between particles.
The force is modeled as an attractive force proportional to the product 
of the masses and inversely proportional to the square of the distance.

Observation:
The model behaves as expected, following Newton's Law of Universal Gravitation. 
However, it often leads to chaotic systems. When particles get too close or 
the G constant is too large, velocities increase rapidly, making the 
simulation move from a velocity of ~10 units/dt to over 2000 units/dt.
"""

from view import *
from model import Vec, Particle, gravitational_force, wall_collision # Importera specifika delar
import math

# 1. Skapa partiklar (t.ex. 4 stycken i en diamantform)
n = 4
positions = [[-5, 0], [0, 5], [5, 0], [0, -5]]
vel_direction = [[1, 1], [1, -1], [-1, -1], [-1, 1]]
particles = []

for i in range(n):
    pos_vec = Vec(positions[i][0], positions[i][1])
    vel_vec = 5 * Vec(vel_direction[i][0], vel_direction[i][1]) 
    particles.append(Particle(1, pos_vec, vel_vec, 1))

# 2. Skapa väggar för simuleringen (valfritt tillägg för realism)
walls(canvas, particles[0].radius) 

# 3. Definiera konstanter
G_CONSTANT = 500
TIME_STEP = 0.0001

# 4. STARTA SIMULERINGEN
# Istället för en egen 'forces'-funktion använder vi en lambda för att
# anropa gravitational_force direkt med parametern G.
# Vi inkluderar även wall_collision för att partiklarna inte ska flyga iväg.

simulation_loop(
    lambda dt, pts: (
        gravitational_force(dt, pts, G_CONSTANT),
        wall_collision(pts, Vec(-1, 0), Vec(8, 0)),
        wall_collision(pts, Vec(1, 0), Vec(-8, 0)),
        wall_collision(pts, Vec(0, -1), Vec(0, 8)),
        wall_collision(pts, Vec(0, 1), Vec(0, -8))
    ), 
    TIME_STEP, 
    particles
)