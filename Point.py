from Vectors import Vector

class Point:
    def __init__(self, coords):
        self.coords = coords

    def to_vector(self):
        return Vector(self.coords)

    def translate(self, vector):
        return Point([a + b for a, b in zip(self.coords, vector.coords)])

    def distance_to(self, other):
        return Vector(self.coords).distance(Vector(other.coords))

    def vector_to(self, other):
        return Vector([b - a for a, b in zip(self.coords, other.coords)])

    def __repr__(self):
        return f"Point({self.coords})"
