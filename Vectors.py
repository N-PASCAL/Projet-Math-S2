from Tools import sqrt, cos, sin

class Vector:
    def __init__(self, coords):
        self.coords = coords

    def __add__(self, other):
        return Vector([a + b for a, b in zip(self.coords, other.coords)])

    def __sub__(self, other):
        return Vector([a - b for a, b in zip(self.coords, other.coords)])

    def __mul__(self, scalar):
        return Vector([scalar * x for x in self.coords])

    def dot(self, other):
        return sum(a * b for a, b in zip(self.coords, other.coords))

    def cross(self, other):
        x1, y1, z1 = self.coords
        x2, y2, z2 = other.coords
        return Vector([
            y1*z2 - z1*y2,
            z1*x2 - x1*z2,
            x1*y2 - y1*x2
        ])

    def norm(self):
        return sqrt(sum(x**2 for x in self.coords))

    def normalize(self):
        n = self.norm()
        if n == 0:
            raise ValueError("Vecteur nul non normalisable")
        return Vector([x / n for x in self.coords])

    def distance(self, other):
        return (self - other).norm()

    def rotate(self, axis, angle):
        x, y, z = self.coords
        c = cos(angle)
        s = sin(angle)
        if axis == 'x':
            return Vector([x, c * y - s * z, s * y + c * z])
        elif axis == 'y':
            return Vector([c * x + s * z, y, -s * x + c * z])
        elif axis == 'z':
            return Vector([c * x - s * y, s * x + c * y, z])
        else:
            raise ValueError("Axe inconnu : choisir 'x', 'y' ou 'z'")

    def angle_with(self, other):
        return cos(self.dot(other) / (self.norm() * other.norm()))

    def project_onto(self, other):
        other_unit = other.normalize()
        scalar_proj = self.dot(other_unit)
        return other_unit * scalar_proj

    def __repr__(self):
        return f"Vector({self.coords})"

