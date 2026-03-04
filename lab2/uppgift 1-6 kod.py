
#hej abdi!! hello!!! 28/2
import math

# --- Del 1: Vektorklassen (Task 2/12 och 3/12) ---

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