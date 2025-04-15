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

def generate_trapeze(n, base_large, base_etroite, hauteur, epaisseur, offset=(0,0,0)):
    T = Geometry.trapeze_plein(n, base_large, base_etroite, hauteur, epaisseur)
    for i in range(len(T[0])):
        T[0][i] += offset[0]
        T[1][i] += offset[1]
        T[2][i] += offset[2]
    return T

def generate_trapeze_custom(n, p1, p2, p3, p4, epaisseur):
    T = Geometry.trapeze_volume(n, p1, p2, p3, p4, epaisseur)
    return T

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

    aile_g = generate_trapeze_custom(n_ailes, p1=[0, 2, 0], p2=[5.5, 2, 0], p3=[2.75, 13.5, 0], p4=[0, 15, 0], epaisseur=0.5)
    aile_d = generate_trapeze_custom(n_ailes, p1=[0, -2, 0], p2=[5.5, -2, 0], p3=[2.75, -13.5, 0], p4=[0, -15, 0], epaisseur=0.5)

    emp_g = generate_trapeze_custom(n_empennages, p1=[-13, 2, 0], p2=[-10.5, 2, 0], p3=[-11.75, 5.5, 0], p4=[-13, 6.5, 0], epaisseur=0.5)
    emp_d = generate_trapeze_custom(n_empennages, p1=[-13, -2, 0], p2=[-10.5, -2, 0], p3=[-11.75, -5.5, 0], p4=[-13, -6.5, 0], epaisseur=0.5)

    derive = generate_trapeze_custom(n_derive, p1=[-13, 0, 2], p2=[-13, 0, 7], p3=[-10.25, 0, 5.75], p4=[-7.5, 0, 2], epaisseur=0.5)

    all_parts = [fuselage, cone_av, cone_ar, aile_g, aile_d, emp_g, emp_d, derive]
    X, Y, Z = [], [], []
    for part in all_parts:
        X += part[0]
        Y += part[1]
        Z += part[2]

    return Matrix([X, Y, Z])

def plot_solide(n):
    M = solide(n)
    M = M.rotate('z', pi / 4) 

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



#-----------------------------------------------------------------------------------------------------------------#

def interactive_plot(n):
    M = solide(n)
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    scatter = ax.scatter3D(*M.data, c=M.data[2], cmap='plasma', s=0.5)

    def update_display():
        X, Y, Z = M.data
        scatter._offsets3d = (X, Y, Z)
        fig.canvas.draw_idle()

    def on_key(event):
        nonlocal M
        angle = pi / 36 
        step = 1.0     
        
        match event.key:
            case 'left':
                M = M.rotate('z', angle)
            case 'right':
                M = M.rotate('z', -angle)
            case 'up':
                M = M.rotate('y', angle)
            case 'down':
                M = M.rotate('y', -angle)
            case '5':
                M = M.translate(dx=step)
            case '2':
                M = M.translate(dx=-step)
            case '1':
                M = M.translate(dy=step)
            case '3':
                M = M.translate(dy=-step)
            case 'r':
                M = solide(n)
            case _:
                return  

        update_display()


    ax.set_box_aspect([55, 40, 10])  
    ax.set_xlim(-30, 30)
    ax.set_ylim(-25, 25) 
    ax.set_zlim(-5, 5)

    fig.canvas.mpl_connect('key_press_event', on_key)
    plt.title("Utilise les flèches pour faire pivoter l'avion")
    plt.show()

#-----------------------------------------------------------------------------------------------------------------#
