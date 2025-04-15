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

        for z in range(n2):
            for r in range(1, n2): 
                for teta in range(n2):
                    x = r * dr * cos(dteta * teta)
                    y = r * dr * sin(dteta * teta)
                    z_val = z * dz + zmin
                    W.append([x, y, z_val])
        return Geometry.transpose(W)

    @staticmethod
    def trapeze_plein(n, base_large, base_etroite, hauteur, epaisseur):
        W = []
        n2 = int(n ** (1 / 3))
        for i in range(n2):
            for j in range(n2):
                for k in range(n2):
                    ratio = i / n2  
                    largeur = base_large * (1 - ratio) + base_etroite * ratio
                    y = -largeur / 2 + largeur * j / n2
                    z = -epaisseur / 2 + epaisseur * k / n2
                    x = -hauteur / 2 + hauteur * i / n2
                    W.append([x, y, z])
        return Geometry.transpose(W)

    @staticmethod
    def trapeze_volume(n, p1, p2, p3, p4, epaisseur):
        from Vectors import Vector
        from Point import Point

        P1, P2, P3, P4 = [Vector(p) if not isinstance(p, Vector) else p for p in [p1, p2, p3, p4]]
        
        n2 = int(n ** (1/3))
        W = []

        for i in range(n2):  
            for j in range(n2):  
                t1 = j / (n2 - 1)
                t2 = i / (n2 - 1)

                A = P1 * (1 - t1) + P2 * t1
                B = P4 * (1 - t1) + P3 * t1

                point_surface = A * (1 - t2) + B * t2

                for k in range(n2):  
                    normal = (P2 - P1).cross(P4 - P1).normalize()
                    depth = -epaisseur / 2 + epaisseur * k / n2
                    P = point_surface + normal * depth
                    W.append(P.coords)

        return Geometry.transpose(W)


    @staticmethod
    def solide(n):
        n_fuselage = int(n * 0.4)
        n_ailes = int(n * 0.3)
        n_queue = int(n * 0.3)

        fuselage = Geometry.cylindre(n_fuselage, R=0.3, h=4)

        ailes_gauche = Geometry.pave_plein(n_ailes // 2, a=2, b=0.1, c=0.02)
        ailes_droite = Geometry.pave_plein(n_ailes // 2, a=2, b=0.1, c=0.02)

        for i in range(len(ailes_gauche[0])):
            ailes_gauche[1][i] -= 0.4  
            ailes_gauche[2][i] -= 0.5  
        for i in range(len(ailes_droite[0])):
            ailes_droite[1][i] += 0.4  
            ailes_droite[2][i] -= 0.5  #

        queue = Geometry.pave_plein(n_queue, a=0.1, b=0.02, c=0.6)
        for i in range(len(queue[0])):
            queue[0][i] -= 1.8 
            queue[2][i] += 0.5  

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
