from matplotlib import pyplot as plt

from Matrix import *
from Tools import *
from Geometry import Geometry

from Solide import plot_solide, interactive_plot


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
# Geometry

#-----------------------------------------------------------------------------------------------------------------#

# renderPlane()
# plot_solide(10000)

interactive_plot(10000)



