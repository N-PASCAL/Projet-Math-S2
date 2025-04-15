from Vectors import Vector

class Geometry:
    def center_of_mass(self, points, masses):
        if len(points) != len(masses):
            raise ValueError("Le nombre de points doit être égal au nombre de masses")

        total_mass = sum(masses)
        if total_mass == 0:
            raise ValueError("La masse totale ne peut pas être nulle")

        weighted_sum = [0, 0, 0]
        for p, m in zip(points, masses):
            weighted_sum = [w + m * x for w, x in zip(weighted_sum, p.coords)]

        return Vector([x / total_mass for x in weighted_sum])

    def moment(self, F, r):
        return r.cross(F)

    def triple_scalar(self, a, b, c):
        return a.dot(b.cross(c))

    def is_colinear(self, v1, v2):
        cross_prod = v1.cross(v2)
        return cross_prod.norm() < 1e-6
