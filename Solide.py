from Geometry import Geometry
from Matrix import Matrix
from Tools import pi, cos, sin
from matplotlib import pyplot as plt

def generate_fuselage(n):
    fuselage = Geometry.cylindre(n, R=2.0, h=26)
    X, Y, Z = fuselage

    return [Z, Y, X]

def generate_cone(n, length, R, reverse=False, offset=0):
    W = []
    n2 = int(n ** (1/3))
    for i in range(n2):
        for j in range(n2):
            for k in range(n2):
                r = R * i / n2
                theta = 2 * pi * j / n2
                x = (length * (1 - i / n2)) if not reverse else (-length * (1 - i / n2))
                x += offset
                y = r * cos(theta)
                z = r * sin(theta)
                W.append([x, y, z])
    return Geometry.transpose(W)

def generate_prism(n, a, b, c, offset=(0,0,0)):
    P = Geometry.pave_plein(n, a, b, c)
    for i in range(len(P[0])):
        P[0][i] += offset[0]
        P[1][i] += offset[1]
        P[2][i] += offset[2]
    return P

def solide(n):
    unit = n // 17  

    n_fuselage = 4 * unit        
    n_cones = 2 * unit          
    n_ailes = 2 * unit          
    n_empennages = 2 * unit      
    n_derive = n - (n_fuselage + 2*n_cones + 2*n_ailes + 2*n_empennages)  

    print("n_fuselage =", n_fuselage)
    print("n_cones =", n_cones)
    print("n_ailes =", n_ailes)
    print("n_empennages =", n_empennages)
    print("n_derive =", n_derive)



    fuselage = generate_fuselage(n_fuselage)

    cone_av = generate_cone(n_cones, length=6.5, R=2.0, reverse=True, offset=-13)
    cone_ar = generate_cone(n_cones, length=7.0, R=2.0, reverse=False, offset=12)

    aile_g = generate_prism(n_ailes, 5.5, 15.0, 0.5, offset=(0, 10, 0))  
    aile_d = generate_prism(n_ailes, 5.5, 15.0, 0.5, offset=(0, -8, 0))   


    emp_g = generate_prism(n_empennages, 2.5, 6.5, 0.5, offset=(-12, 6, -0))
    emp_d = generate_prism(n_empennages, 2.5, 6.5, 0.5, offset=(-12, -6, 0))


    derive = generate_prism(n_derive, 5.5, 0.5, 4.375, offset=(-11, 0, 4))


    all_parts = [fuselage, cone_av, cone_ar, aile_g, aile_d, emp_g, emp_d, derive]
    X, Y, Z = [], [], []
    for part in all_parts:
        X += part[0]
        Y += part[1]
        Z += part[2]

    return Matrix([X, Y, Z])

def plot_solide(n):
    M = solide(n)
    X, Y, Z = M.data

    fig = plt.figure()
    ax = plt.axes(projection='3d')
    ax.scatter3D(X, Y, Z, c=Z, cmap='plasma', s=0.5)

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title(f'Solide réaliste - {n} points')

    
    ax.set_box_aspect([55, 40, 10])  
    ax.set_xlim(-30, 30)
    ax.set_ylim(-25, 25) 
    ax.set_zlim(-5, 5)

    plt.tight_layout()
    plt.show()
