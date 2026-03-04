"""

In this experiment file we will showcase the gravity mechanic of our simulation.
The gravity is modeled as a attractive force, proportional to the distance between particles radius
In order to see clearly, one of the particles will be highlighted with color and a vel vector.


The model behaves as expected, however it does often go towards a form of chaos. When the
particles gets to close or the G constant is too large, their velocities increase to the point
that tracking them on the screen becomes impossible. From  a vel of around 10 units / dt to
well over 2000.
"""


from view import *
import math

#create 4 particles in a diamond shape shape
n = 4
positions = [[-5,0],[0,5],[5,0],[0,-5]]
vel_direction = [[1,1],[1,-1],[-1,-1],[-1,1]]
particles = []
for i in range(n):
    pos_vec = Vec(positions[i][0],positions[i][1])
    vel_vec = 5 * Vec(vel_direction[i][0],vel_direction[i][1]) 
    particles.append(Particle(1,pos_vec,vel_vec,1))


# create the walls of the simulation
walls(canvas,particles[0].radius) 

def forces(dt,particles): # the forces that will act
   gravitational_force(dt,particles,500)
   wall_collision(particles,Vec(-1,0),Vec(8,0))
   wall_collision(particles,Vec(1,0),Vec(-8,0))
   wall_collision(particles,Vec(0,-1),Vec(0,8))
   wall_collision(particles,Vec(0,1),Vec(0,-8))

simulation_loop(forces, 0.0001, particles) # run simulation

