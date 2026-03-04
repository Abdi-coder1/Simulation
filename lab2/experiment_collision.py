"""
In this experiment file we will showcase the collision mechanic of our simulation.
The collision is modeled as a repulsive force, proportional to the radius of the particles.
In order to see clearly, one of the particles will be highlighted.


The simulation acted as expected most of the time. When particles collide, they get pushed apart.
But to our surprise, the collision doesn't happen instantly. Since we are approximating
it is a repulsive force, it takes time for it to act and change direction. 
Which has the effectthat particles tend to go into each other a bit. 
Adding to this observation. If the collision factor k, is too small, 
particles will tend to pass each other instead!
 And the same k factor may not workif the radius changes or if the velocities are too big. 

A future improvement could be a dynamic k value that changes based on radius and velocity. 

Notice that we use a collision wall isntead of the wall force, to make it more realistic
"""


from view import *
import math

#create particles in a circular pattern with one of color
n = 5
particles = []
for i in range(n):
    theta = i*2*math.pi/n
    u = Vec(math.cos(theta),math.sin(theta))
    pos = 5 * u
    vel = -10 * u 
    particles.append(Particle(1,pos,vel,1))
colors= ['blue' for i in range(len(particles))]
colors[i] = 'yellow'

# create the walls of the simulation
walls(canvas,particles[0].radius) 

def forces(dt,particles):
   
   collision(dt,particles,500) # collsion
   wall_collision(particles,Vec(-1,0),Vec(8,0))
   wall_collision(particles,Vec(1,0),Vec(-8,0))
   wall_collision(particles,Vec(0,-1),Vec(0,8))
   wall_collision(particles,Vec(0,1),Vec(0,-8))

simulation_loop(forces, 0.0001, particles)

"""
The time step has a clear visual effect on the simulation. To large
and the it becomes jagged, with to much distance beeing covered in the time frame.
This has the added dowside that it glitches out of the wall. In contrats, to small
and it becomes very slow, with no real effetc beings observed.
Recomendation: 10^(-3)--> 10^(-5) i
"""
