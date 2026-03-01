from view import *
import math

n = 20
particles = []
for i in range(n):
    theta = i*2*math.pi/n
    u = Vec(math.cos(theta),math.sin(theta))
    pos = 10 * u
    vel = -1 * u 
    particles.append(Particle(1,pos,vel,0.2))

def circular_arena(dt, particles, k, R):
    for particle in particles:
        r = particle.position.norm()
        if r > R:
            force =k* (R-r)* (1/r) * particle.position
            particle.apply_force(dt, force)
       
def wall_force(dt, particles, k, n, a):
    for particle in particles:
        d = dot((particle.position - a ), n)
        if d<0:
            force = -1*k*d*n
            particle.apply_force(dt, force)

def forces(dt,particles):
    wall_force(dt,particles,5,Vec(-1,0),Vec(5,0))
    wall_force(dt,particles,5,Vec(1,0),Vec(-5,0))
    



simulation_loop(forces, 0.0005, particles)
