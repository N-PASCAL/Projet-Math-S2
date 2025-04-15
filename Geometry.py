from Vectors import Vector
from Tools import *
class Geometry:

    @staticmethod
    def transpose(A):
        return [[A[i][j] for i in range(len(A))] for j in range(len(A[0]))]

    @staticmethod
    def carre_plein(n, a):
        W = []
        n2 = int(n ** (1 / 2))
        dx = a / n2
        xmin = -a / 2
        for x in range(n2):
            for y in range(n2):
                W.append([dx * x + xmin, dx * y + xmin, 0])
        return Geometry.transpose(W)

    @staticmethod
    def pave_plein(n, a, b, c):
        W = []
        n2 = int(n ** (1 / 3))
        dx, dy, dz = a / n2, b / n2, c / n2
        xmin, ymin, zmin = -a / 2, -b / 2, -c / 2
        for x in range(n2):
            for y in range(n2):
                for z in range(n2):
                    W.append([dx * x + xmin, dy * y + ymin, dz * z + zmin])
        return Geometry.transpose(W)

    @staticmethod
    def cylindre(n, R, h):
        W = []
        n2 = int(n ** (1 / 3))
        dr = R / n2
        dteta = 2 * pi / n2
        dz = h / n2
        zmin = -h / 2
        for r in range(n2):
            for teta in range(n2):
                for z in range(n2):
                    x = r * dr * cos(dteta * teta)
                    y = r * dr * sin(dteta * teta)
                    z_val = z * dz + zmin
                    W.append([x, y, z_val])
        return Geometry.transpose(W)

    @staticmethod
    def solide(n):
        # Proportions des différentes parties
        n_fuselage = int(n * 0.4)
        n_ailes = int(n * 0.3)
        n_queue = int(n * 0.3)

        # Fuselage central : cylindre long et fin, initialement orienté sur Z
        fuselage = Geometry.cylindre(n_fuselage, R=0.3, h=4)

        # Rotation du fuselage pour l’orienter sur l’axe X
        for i in range(len(fuselage[0])):
            v = Vector([fuselage[0][i], fuselage[1][i], fuselage[2][i]])
            v_rotated = v.rotate('y', -pi / 2)
            fuselage[0][i], fuselage[1][i], fuselage[2][i] = v_rotated.coords


        # Ailes : pavés plats, décalés sur l'axe Y
        ailes_gauche = Geometry.pave_plein(n_ailes // 2, a=2, b=0.1, c=0.02)
        ailes_droite = Geometry.pave_plein(n_ailes // 2, a=2, b=0.1, c=0.02)

        # Décalage des ailes : à gauche et à droite du fuselage
        for i in range(len(ailes_gauche[0])):
            ailes_gauche[1][i] -= 0.4  # Y vers la gauche
            ailes_gauche[2][i] -= 0.5  # Z pour les coller à la bonne hauteur
        for i in range(len(ailes_droite[0])):
            ailes_droite[1][i] += 0.4  # Y vers la droite
            ailes_droite[2][i] -= 0.5  # Z aussi

        # Queue verticale : petit pavé vertical à l'arrière
        queue = Geometry.pave_plein(n_queue, a=0.1, b=0.02, c=0.6)
        for i in range(len(queue[0])):
            queue[0][i] -= 1.8  # X vers l’arrière
            queue[2][i] += 0.5  # Z en hauteur

        # Fusionner toutes les matrices
        X = fuselage[0] + ailes_gauche[0] + ailes_droite[0] + queue[0]
        Y = fuselage[1] + ailes_gauche[1] + ailes_droite[1] + queue[1]
        Z = fuselage[2] + ailes_gauche[2] + ailes_droite[2] + queue[2]

        return [X, Y, Z]

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
