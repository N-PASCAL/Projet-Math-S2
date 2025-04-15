from Vectors import Vector
from Matrix import Matrix

class Physics:
    def acceleration(self, force, mass):
        if mass == 0:
            raise ValueError("La masse ne peut pas être nulle.")
        return force * (1 / mass)

    def angular_acceleration(self, moment, inertia_matrix):
        I_inv = inertia_matrix.inverse()
        return I_inv * Matrix([[x] for x in moment.coords])

    def deplace_mat(self, I, m, G, A):
        d = G.vector_to(A).coords
        d_matrix = Matrix([
            [0, -d[2], d[1]],
            [d[2], 0, -d[0]],
            [-d[1], d[0], 0]
        ])
        dT_d = d_matrix * d_matrix.transpose()
        return I + (m * dT_d)
