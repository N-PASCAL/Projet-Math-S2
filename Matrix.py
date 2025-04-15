from Tools import cos, sin

class Matrix:
    def __init__(self, data):
        # Vérifie que toutes les lignes ont la même longueur
        first_row_length = len(data[0])
        for row in data:
            if len(row) != first_row_length:
                raise ValueError("Toutes les lignes doivent avoir la même longueur.")
        self.data = data

    # Renvoie le nombre de lignes et de colonnes
    def shape(self):
        nb_lignes = len(self.data)
        nb_colonnes = len(self.data[0])
        return nb_lignes, nb_colonnes

    # Transpose la matrice 
    def transpose(self):
        lignes, colonnes = self.shape()
        resultat = []
        for j in range(colonnes):
            ligne = []
            for i in range(lignes):
                ligne.append(self.data[i][j])
            resultat.append(ligne)
        return Matrix(resultat)

    # Produit scalaire ou produit matriciel, surcharge l'opérateur *
    def __mul__(self, other):
        if isinstance(other, (int, float)):     # isinstance permet de vérifier le type de l'objet, donc de déuduire si c'est un int, un float ou une Matrix
            # Multiplication par un scalaire
            resultat = []
            for ligne in self.data:
                nouvelle_ligne = []
                for valeur in ligne:
                    nouvelle_ligne.append(valeur * other)
                resultat.append(nouvelle_ligne)
            return Matrix(resultat)

        elif isinstance(other, Matrix):
            # Multiplication entre matrices
            a_lignes, a_colonnes = self.shape()
            b_lignes, b_colonnes = other.shape()

            if a_colonnes != b_lignes:
                raise ValueError("Multiplication impossible : dimensions incompatibles")

            resultat = []
            for i in range(a_lignes):
                ligne = []
                for j in range(b_colonnes):
                    somme = 0
                    for k in range(a_colonnes):
                        somme += self.data[i][k] * other.data[k][j]
                    ligne.append(somme)
                resultat.append(ligne)
            return Matrix(resultat)
        else:
            raise ValueError("Multiplication non supportée")


    def __rmul__(self, other):
        return self * other

    # Déterminant (récursif)
    def determinant(self):
        A = self.data
        if len(A) == 1:
            return A[0][0]
        total = 0
        for i in range(len(A)):
            signe = (-1) ** i
            sous_matrice = Matrix.pop(A, i, 0)
            mineur = Matrix(sous_matrice).determinant()
            total += signe * A[i][0] * mineur
        return total

    # Calcule la comatrice
    def comatrix(self):
        A = self.data
        resultat = []
        for i in range(len(A)):
            ligne = []
            for j in range(len(A[0])):
                signe = (-1) ** (i + j)
                sous_matrice = Matrix.pop(A, i, j)
                mineur = Matrix(sous_matrice).determinant()
                ligne.append(signe * mineur)
            resultat.append(ligne)
        return Matrix(resultat)

    # Inverse la matrice si possible
    def inverse(self):
        d = self.determinant()
        if d == 0:
            raise ValueError("La matrice n'est pas inversible.")
        comatrice = self.comatrix()
        transposee = comatrice.transpose()
        inverse = transposee * (1 / d)
        return inverse

    # Supprime une ligne et une colonne d'une matrice
    @staticmethod
    def pop(A, i, j):
        nouvelle_matrice = []
        for ligne_index in range(len(A)):
            if ligne_index != i:
                nouvelle_ligne = []
                for col_index in range(len(A[0])):
                    if col_index != j:
                        nouvelle_ligne.append(A[ligne_index][col_index])
                nouvelle_matrice.append(nouvelle_ligne)
        return nouvelle_matrice

    # Affiche joliment la matrice
    def __str__(self):
        lignes = []
        for ligne in self.data:
            texte = "\t".join(str(round(valeur, 2)) for valeur in ligne)
            lignes.append(texte)
        return "\n".join(lignes)
    
    def rotate(self, axis, angle):
        if self.shape()[0] != 3:
            raise ValueError("La rotation ne s'applique qu'aux matrices 3×n")

        c = cos(angle)
        s = sin(angle)

        if axis == 'x':
            R = Matrix([
                [1, 0, 0],
                [0, c, -s],
                [0, s, c]
            ])
        elif axis == 'y':
            R = Matrix([
                [c, 0, s],
                [0, 1, 0],
                [-s, 0, c]
            ])
        elif axis == 'z':
            R = Matrix([
                [c, -s, 0],
                [s, c, 0],
                [0, 0, 1]
            ])
        else:
            raise ValueError("Axe inconnu : choisir 'x', 'y' ou 'z'")

        return R * self 

    def translate(self, dx=0, dy=0, dz=0):
        if self.shape()[0] != 3:
            raise ValueError("La translation ne s'applique qu'à une matrice 3×n")

        X, Y, Z = self.data
        X = [x + dx for x in X]
        Y = [y + dy for y in Y]
        Z = [z + dz for z in Z]
        return Matrix([X, Y, Z])



def transpose(A):
    if not isinstance(A, Matrix):
        raise TypeError("transpose attend une instance de Matrix.")
    return A.transpose()

def determinant(A):
    if not isinstance(A, Matrix):
        raise TypeError("determinant attend une instance de Matrix.")
    return A.determinant()

def comatrix(A):
    if not isinstance(A, Matrix):
        raise TypeError("comatrix attend une instance de Matrix.")
    return A.comatrix()

def inverse(A):
    if not isinstance(A, Matrix):
        raise TypeError("inverse attend une instance de Matrix.")
    return A.inverse()

__all__ = ["Matrix", "transpose", "determinant", "comatrix", "inverse"]
