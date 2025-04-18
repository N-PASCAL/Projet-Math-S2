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
        def vec_add(a, b): return [a[i] + b[i] for i in range(3)]
        def vec_sub(a, b): return [a[i] - b[i] for i in range(3)]
        def vec_scale(a, s): return [a[i] * s for i in range(3)]
        def vec_dot(a, b): return sum(a[i] * b[i] for i in range(3))
        def vec_cross(a, b):
            return [
                a[1]*b[2] - a[2]*b[1],
                a[2]*b[0] - a[0]*b[2],
                a[0]*b[1] - a[1]*b[0]
            ]
        def vec_norm(v): return sum(x**2 for x in v) ** 0.5
        def vec_normalize(v):
            norm = vec_norm(v)
            return [x / norm for x in v] if norm != 0 else [0, 0, 0]

        n2 = int(n ** (1/3))
        W = []

        for i in range(n2):
            for j in range(n2):
                t1 = j / (n2 - 1)
                t2 = i / (n2 - 1)

                A = vec_add(vec_scale(p1, 1 - t1), vec_scale(p2, t1))
                B = vec_add(vec_scale(p4, 1 - t1), vec_scale(p3, t1))
                point_surface = vec_add(vec_scale(A, 1 - t2), vec_scale(B, t2))

                normal = vec_cross(vec_sub(p2, p1), vec_sub(p4, p1))
                normal = vec_normalize(normal)

                for k in range(n2):
                    depth = -epaisseur / 2 + epaisseur * k / n2
                    P = vec_add(point_surface, vec_scale(normal, depth))
                    W.append(P)

        return Geometry.transpose(W)

