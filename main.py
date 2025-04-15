from matplotlib import pyplot as plt

from Matrix import *
from Tools import *
from Geometry import Geometry

from Solide import plot_solide


#-----------------------------------------------------------------------------------------------------------------#
""" 
    Tools.py
    - pi : constante mathématique
    - fact(n) : calcule la factorielle de n (n!)
    - cos(x) : calcule le cosinus de x avec la série de Taylor
    - sin(x) : calcule le sinus de x avec la série de Taylor
    - sqrt(x) : racine carrée de x (Newton-Raphson)
    - abs(x) : valeur absolue
    - deg2rad(deg) : convertit degrés → radians
    - rad2deg(rad) : convertit radians → degrés

    Matrix.py
    - Matrix : classe de matrice
    - shape() : dimensions
    - transpose() : transposée
    - __mul__ : produit scalaire/matriciel
    - determinant() : calcul récursif
    - comatrix() : cofacteurs
    - inverse() : inverse par comatrice
    - __str__() : affichage joli
    - pop(A, i, j) : extrait une sous-matrice
"""

# Exemple d'utilisation des differents fichiers :
# -----------------------------------------------
"""
# MATRIX
A = Matrix([[1, 2, 3], [9, 1, 1], [5, 6, 7]])
B = Matrix([[1, 2], [3, 4], [5, 6]])
print("A =\n", A)
print("Transpose(A) =\n", transpose(A))
print("Comatrice(A) =\n", comatrix(A))
print("Inverse(A) =\n", inverse(A))
print("Déterminant(A) =", determinant(A))
print("Produit B * A =\n", B * A)
"""

# -----------------------------------------------
"""
# Tools
print("cos(pi) =", cos(pi))
print("sin(pi/2) =", sin(pi / 2))
print("sqrt(16) =", sqrt(16))
print("fact(5) =", fact(5))
print("deg2rad(180) =", deg2rad(180))
print("rad2deg(pi) =", rad2deg(pi))
"""
# -----------------------------------------------
<<<<<<< HEAD
# Geometry

=======
# VECTOR
"""
v1 = Vector([1, 0, 0])
v2 = Vector([0, 1, 0])
print("v1 + v2 =", v1 + v2)
print("v1 ⋅ v2 =", v1.dot(v2))
print("v1 × v2 =", v1.cross(v2))
print("norm(v1) =", v1.norm())
print("v1 rotated around Z (90°) =", v1.rotate('z', pi / 2))
print("Angle v1-v2 (cos) =", v1.angle_with(v2))
print("Projection v1 sur v2 =", v1.project_onto(v2))
"""

# -----------------------------------------------
# POINT
"""
p1 = Point([1, 2, 3])
p2 = Point([4, 5, 6])
print("Distance p1 -> p2 =", p1.distance_to(p2))
print("Vecteur p1 -> p2 =", p1.vector_to(p2))
print("Translation de p1 par v1 =", p1.translate(v1))
"""

# -----------------------------------------------
# GEOMETRY UTILS
"""
geo = Geometry()
points = [p1, p2]
masses = [2, 3]
print("Centre d'inertie =", geo.center_of_mass(points, masses))
print("Moment de v1 appliqué en v2 =", geo.moment(v1, v2))
print("Triple scalaire (v1, v2, v1 + v2) =", geo.triple_scalar(v1, v2, v1 + v2))
print("v1 et v2 colinéaires ? ", geo.is_colinear(v1, v2))
"""

# -----------------------------------------------
# PHYSICS UTILS
"""
phys = Physics()
F = Vector([10, 0, 0])
m = 5
print("a = F/m =", phys.acceleration(F, m))

I = Matrix([[2, 0, 0], [0, 3, 0], [0, 0, 4]])
M = Vector([0, 0, 10])
print("alpha = I⁻¹ * M =\n", phys.angular_acceleration(M, I))

G = Point([0, 0, 0])
A = Point([1, 0, 0])
print("I déplacée de G vers A =\n", phys.deplace_mat(I, m, G, A))
"""
>>>>>>> parent of 7fb507b (VFINAL def Solide)
#-----------------------------------------------------------------------------------------------------------------#

plot_solide(10000)

<<<<<<< HEAD


# (X, Y, Z) = Geometry.solide(10000)
# fig = plt.figure()
# ax = plt.axes(projection='3d')
# ax.scatter3D(X, Y, Z, c=Z, cmap='plasma')
# plt.show()


renderPlane()
=======
# renderPlane()
>>>>>>> parent of 7fb507b (VFINAL def Solide)
