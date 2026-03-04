
import math

class Vec:
    """Representerar en 2D-vektor och tillhandahåller matematiska operationer."""
    
    def __init__(self, x, y):
        # Initierar vektorn med koordinaterna x och y
        self.x = x
        self.y = y

    def __repr__(self):
        # Returnerar en sträng som ser ut som (x,y)
        return f"({self.x},{self.y})"

    def __rmul__(self, factor):
        # Skalär multiplikation (t.ex. 5 * v). 
        # Returnerar en NY vektor för att inte ändra på den befintliga.
        return Vec(self.x * factor, self.y * factor)

    def __add__(self, other):
        # Vektoration (v1 + v2). Vi adderar x med x och y med y.
        return Vec(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        # Vektorsubtraktion (v1 - v2).
        return Vec(self.x - other.x, self.y - other.y)

    def norm(self):
        # Beräknar den euklidiska normen (längden) enligt formeln sqrt(x^2 + y^2)
        return math.sqrt(self.x**2 + self.y**2)

    def get_coords(self):
        # Returnerar koordinaterna som en tuple
        return (self.x, self.y)

def dot(u, v):
    """Beräknar skalärprodukten (dot product) av två vektorer u och v."""
    # Formel: u_x * v_x + u_y * v_y
    return u.x * v.x + u.y * v.y


# --- Del 2: Partikelklassen (Task 4/12, 5/12 och 6/12) ---

class Particle:
    """Representerar en partikel med massa, position, hastighet och radie."""
    
    def __init__(self, mass, position, velocity, radius):
        # Notera: position och velocity förväntas vara Vec-objekt
        self.mass = mass
        self.position = position
        self.velocity = velocity
        self.radius = radius

    def inertial_move(self, dt):
        """
        Uppdaterar positionen baserat på hastighet över tiden dt.
        Formel: x_ny = x_0 + v * dt
        """
        # Eftersom vi definierat __add__ och __rmul__ i Vec-klassen 
        # kan vi skriva detta väldigt likt den matematiska formeln.
        self.position = self.position + (dt * self.velocity)

    def apply_force(self, dt, f):
        """
        Uppdaterar hastigheten baserat på en kraft f över tiden dt.
        Enligt F = ma => a = f / m
        Hastighetsändring: v_ny = v_0 + a * dt => v_ny = v_0 + (f / m) * dt
        """
        # Beräkna accelerationen (a = f / m)
        acceleration = (1 / self.mass) * f
        
        # Uppdatera hastigheten: v = v + a * dt
        self.velocity = self.velocity + (dt * acceleration)


    def bounding_box(self):
        """
        Given the current particale, what is it's bounding box? Represented by two 
        vectors, top-leaft and lower-right.
        """
        top_left_vector =  Vec(self.position.x - self.radius, self.position.y + self.radius)
        bottom_right_vector = Vec(self.position.x + self.radius, self.position.y - self.radius)

        return [top_left_vector,bottom_right_vector]

# Custom forces for this simulation

def circular_arena(dt, particles, k, R):
    # A force that directs particles ouside the cicular arena towards the center, proportionally 
    for particle in particles:
        r = particle.position.norm()
        if r > R: # outside arena
            force =-1*k* (r-R)* (1/r) * particle.position
            particle.apply_force(dt, force)
       
def wall_collision(particles, n, a):
    """ 
    With a ancor vector (a) an a normal vector (n),
    we define a straight wall. On wich particles may bounce with
    perfect elastic collision. Particles on the negative side are allowed passages.
    """
    for particle in particles:
       d = particle.position - a 
       if dot(d,n)<=0: # coliding on the wall, or on the negative side of it. 
            if  dot(particle.velocity,n)<0: # moving away from the wall
                particle.velocity  = particle.velocity - \
                            2 * ((dot(particle.velocity,n))/(dot(n,n))) * n
                
def Vec_sum(vec_list):
     # Output the sum of the vectors in the list
    if vec_list:
        vec_sum = vec_list[0]
        for i in range(1,len(vec_list)):
            vec_sum+=vec_list[i]
        return vec_sum
    else:
        return None
            

def gravitational_force(dt, particles, G):
    """
    Implement Newtons law of gravity, by calculating each gravity force pairwise,
    and then applying it. 
    """
    n = len(particles)
    if n>=2: # gravity requires 2 partciles at least
        gravity_forces = [[] for _ in range(n)] # contains the grav force for each particle
        for i in range(n):
            particle1 = particles[i]
            for j in range(i+1,n):
                particle2 = particles[j]
                #Use newtons law of gravity
                distance_vec = (particle2.position-particle1.position)
                force_amount = (G * particle1.mass*particle2.mass) / distance_vec.norm()**2 
                force = (force_amount * (1/distance_vec.norm())) * distance_vec

                # parwise placement by newtons third law of motion
                gravity_forces[i].append(force)
                gravity_forces[j].append(-1*force)

        for i in range(n):  #sum up the forces ann aplly them
            total_grav_force = Vec_sum(gravity_forces[i])
            particles[i].apply_force(dt,total_grav_force)
  
def collision(dt, particles, k):
    """
    Collision can be modeld by a repulsive field for each particle,
    that activates on contact. Utilizes same logic as gravity.
    """
    n = len(particles)
    if n>=2:
        repulsive_forces = [[] for _ in range(n)]
        for i in range(n):
            particle1 = particles[i]
            for j in range(i+1,n):
                particle2 = particles[j]
                distance_vec = (particle2.position-particle1.position)
                if distance_vec.norm() <= particle1.radius + particle2.radius: # collisionm
                        force_amount = k*(particle1.radius + particle2.radius - distance_vec.norm())
                        force = -1*(force_amount * (1/distance_vec.norm())) * distance_vec
                        repulsive_forces[i].append(force)
                        repulsive_forces[j].append(-1*force)
        for i in range(n):
            if repulsive_forces[i]: # is tehre a force to apply?
                total_repulsive_force = Vec_sum(repulsive_forces[i])
                particles[i].apply_force(dt,total_repulsive_force)

