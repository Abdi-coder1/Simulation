import math

class Vec:
    """Representerar en 2D-vektor och tillhandahåller matematiska operationer."""
    
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"({self.x},{self.y})"

    def __rmul__(self, factor):
        # Skalär multiplikation: f * v
        return Vec(self.x * factor, self.y * factor)

    def __add__(self, other):
        # Vektoraddition: v1 + v2
        return Vec(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        # Vektorsubtraktion: v1 - v2
        return Vec(self.x - other.x, self.y - other.y)

    def norm(self):
        # Beräknar längden (euklidisk norm)
        return math.sqrt(self.x**2 + self.y**2)

    def get_coords(self):
        return (self.x, self.y)

def dot(u, v):
    """Beräknar skalärprodukten av två vektorer."""
    return u.x * v.x + u.y * v.y

class Particle:
    """Representerar en partikel med massa, position, hastighet och radie."""
    
    def __init__(self, mass, position, velocity, radius):
        self.mass = mass
        self.position = position  # Vec-objekt
        self.velocity = velocity  # Vec-objekt
        self.radius = radius

    def inertial_move(self, dt):
        """Uppdaterar position baserat på hastighet: x = x0 + v*dt"""
        self.position = self.position + (dt * self.velocity)

    def apply_force(self, dt, f):
        """Uppdaterar hastighet baserat på kraft: v = v0 + (f/m)*dt"""
        acceleration = (1 / self.mass) * f
        self.velocity = self.velocity + (dt * acceleration)

    def bounding_box(self):
        """
        Returnerar partikelns begränsningsrektangel som två VEKTORER 
        (övre vänstra och nedre högra hörnet).
        Korrigerad för att säkerställa att returtypen matchar Vec-objekt.
        """
        top_left = Vec(self.position.x - self.radius, self.position.y + self.radius)
        bottom_right = Vec(self.position.x + self.radius, self.position.y - self.radius)
        return top_left, bottom_right

# --- HJÄLPFUNKTIONER ---

def vec_sum(vec_list):
    """Summerar en lista av vektorer och returnerar ett Vec-objekt."""
    if not vec_list:
        return Vec(0, 0)
    res = Vec(0, 0)
    for v in vec_list:
        res = res + v
    return res

# --- KRAFTER OCH INTERAKTIONER ---

def gravitational_force(dt, particles, G):
    """
    Implementerar Newtons gravitationslag parvis för alla partiklar.
    Används i experiment_gravitational_forces.py.
    """
    n = len(particles)
    if n < 2:
        return

    # Skapa en lista för att samla krafter för varje partikel
    forces_on_particles = [[] for _ in range(n)]

    for i in range(n):
        for j in range(i + 1, n):
            p1 = particles[i]
            p2 = particles[j]
            
            diff = p2.position - p1.position
            r = diff.norm()
            
            if r == 0: continue # Undvik division med noll

            # F = G * (m1 * m2) / r^2
            mag = (G * p1.mass * p2.mass) / (r**2)
            f_vec = (mag / r) * diff
            
            forces_on_particles[i].append(f_vec)
            forces_on_particles[j].append(-1 * f_vec)

    for i in range(n):
        total_f = vec_sum(forces_on_particles[i])
        particles[i].apply_force(dt, total_f)

def collision(dt, particles, k):
    """
    Modellerar kollision som en repulsiv kraft proportionell mot överlappet.
    Används i experiment_elastic_collisions.py.
    """
    n = len(particles)
    forces_on_particles = [[] for _ in range(n)]

    for i in range(n):
        for j in range(i + 1, n):
            p1 = particles[i]
            p2 = particles[j]
            diff = p2.position - p1.position
            dist = diff.norm()
            
            min_dist = p1.radius + p2.radius
            if dist < min_dist and dist > 0:
                # Kraft proportionell mot hur mycket de tryckts ihop
                overlap = min_dist - dist
                mag = k * overlap
                f_vec = -1 * (mag / dist) * diff
                
                forces_on_particles[i].append(f_vec)
                forces_on_particles[j].append(-1 * f_vec)

    for i in range(n):
        total_f = vec_sum(forces_on_particles[i])
        particles[i].apply_force(dt, total_f)

# --- EXTRA FUNKTIONER (FÖR REALISM I EXPERIMENT) ---

def wall_collision(particles, n, a):
    """
    Hanterar studs mot en oändlig vägg definierad av en normal n och en punkt a.
    Lagt till som extra funktionalitet för att hålla partiklar inom synfältet.
    """
    for p in particles:
        d = p.position - a 
        if dot(d, n) <= 0: # Partikeln är vid eller bakom väggen
            if dot(p.velocity, n) < 0: # Rör sig mot väggen
                # Perfekt elastisk studs: v_ny = v - 2 * (v·n / n·n) * n
                p.velocity = p.velocity - 2 * (dot(p.velocity, n) / dot(n, n)) * n