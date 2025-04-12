from Matrix import *
from Tools import *

#-----------------------------------------------------------------------------------------------------------------#
""" 
    Tools.py
    - pi : constante mathématique
    - fact(n) : calcule la factorielle de n (n!)
    - cos(x) : calcule le cosinus de x en utilisant la série de Taylor
    - sin(x) : calcule le sinus de x en utilisant la série de Taylor
    
    Matrix.py
    - Matrix : classe représentant une matrice
    - shape(self) : renvoie le nombre de lignes et de colonnes de la matrice
    - transpose(self) : transpose la matrice
    - __mul__(self, other) : surcharge de l'opérateur * pour la multiplication de matrices ou par un scalaire
    - determinant(self) : calcule le déterminant de la matrice de manière récursive
    - comatrix(self) : calcule la matrice adjointe (comatrice) de la matrice
    - inverse(self) : calcule l'inverse de la matrice
    - __str__(self) : renvoie une représentation sous forme de chaîne de la matrice
    - pop(A, i, j) : supprime la ligne i et la colonne j de la matrice A  
"""
#-----------------------------------------------------------------------------------------------------------------#

# Exemple d'utilisation de la classe Matrix et des fonctions de Tools
"""
A = Matrix([[1, 2, 3], [9, 1, 1], [5, 6, 7]])
B = Matrix([[1, 2], [3, 4], [5, 6]])
C = Matrix([[1, 2], [3, 4]])

print("A =")
print(A)

print("\nTranspose de A =")
print(transpose(A))

print("\nComatrice de A =")
print(comatrix(A))

print("\nInverse de A =")
print(inverse(A))

print("\nDéterminant de A =")
print(determinant(A))

print("\nProduit de B et C =")
print(B * C)

print("\nProduit de 3 et B =")
print(3 * B)

print("\nProduit de B et 3 =")
print(B * 3)

print(cos(pi))
print(sin(pi))
print(fact(5))
"""

#-----------------------------------------------------------------------------------------------------------------#