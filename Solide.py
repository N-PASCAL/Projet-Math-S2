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
    n2 = int(n ** (1 / 3))
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


def generate_prism(n, a, b, c, offset=(0, 0, 0)):
    P = Geometry.pave_plein(n, a, b, c)
    for i in range(len(P[0])):
        P[0][i] += offset[0]
        P[1][i] += offset[1]
        P[2][i] += offset[2]
    return P


def generate_trapeze(n, base_large, base_etroite, hauteur, epaisseur, offset=(0, 0, 0)):
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
    n_derive = n - (n_fuselage + 2 * n_cones + 2 * n_ailes + 2 * n_empennages)

    fuselage = generate_fuselage(n_fuselage)

    cone_av = generate_cone(n_cones, length=6.5, R=2.0, reverse=True, offset=-13)
    cone_ar = generate_cone(n_cones, length=7.0, R=2.0, reverse=False, offset=12)

    aile_g = generate_trapeze_custom(n_ailes, p1=[0, 2, 0], p2=[5.5, 2, 0], p3=[2.75, 13.5, 0], p4=[0, 15, 0],
                                     epaisseur=0.5)
    aile_d = generate_trapeze_custom(n_ailes, p1=[0, -2, 0], p2=[5.5, -2, 0], p3=[2.75, -13.5, 0], p4=[0, -15, 0],
                                     epaisseur=0.5)

    emp_g = generate_trapeze_custom(n_empennages, p1=[-13, 2, 0], p2=[-10.5, 2, 0], p3=[-11.75, 5.5, 0],
                                    p4=[-13, 6.5, 0], epaisseur=0.5)
    emp_d = generate_trapeze_custom(n_empennages, p1=[-13, -2, 0], p2=[-10.5, -2, 0], p3=[-11.75, -5.5, 0],
                                    p4=[-13, -6.5, 0], epaisseur=0.5)

    derive = generate_trapeze_custom(n_derive, p1=[-13, 0, 2], p2=[-13, 0, 7], p3=[-10.25, 0, 5.75], p4=[-7.5, 0, 2],
                                     epaisseur=0.5)

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


# -----------------------------------------------------------------------------------------------------------------#

def deplace_mat(I, m, G, A):
    if len(I) != 3 or any(len(row) != 3 for row in I):
        raise ValueError("I doit être une matrice 3×3")
    if len(G) != 3 or len(A) != 3:
        raise ValueError("G et A doivent être des points 3D")

    d = [A[i] - G[i] for i in range(3)]
    d_norm_sq = sum(d_i ** 2 for d_i in d)

    I3 = [[1 if i == j else 0 for j in range(3)] for i in range(3)]
    d_outer = [[d[i] * d[j] for j in range(3)] for i in range(3)]

    correction = [[m * (d_norm_sq * I3[i][j] - d_outer[i][j]) for j in range(3)] for i in range(3)]
    IA = [[I[i][j] + correction[i][j] for j in range(3)] for i in range(3)]

    return IA


m = 5.0
G = [0.0, 0.0, 0.0]
A = [1.0, 2.0, 3.0]


def calcul_inertie_totale(blocs):
    """
    blocs : liste de dictionnaires avec pour chaque bloc :
        - "m"  : masse
        - "I"  : matrice d'inertie 3x3 (au point G_i)
        - "G"  : centre de masse du bloc [x, y, z]
    """
    from copy import deepcopy

    M_total = sum(bloc["m"] for bloc in blocs)
    A = [0.0, 0.0, 0.0]
    for bloc in blocs:
        for i in range(3):
            A[i] += bloc["m"] * bloc["G"][i]
    A = [coord / M_total for coord in A]

    matrices_deplacees = []
    for bloc in blocs:
        I_dep = deplace_mat(deepcopy(bloc["I"]), bloc["m"], bloc["G"], A)
        matrices_deplacees.append(I_dep)

    I_totale = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    for M in matrices_deplacees:
        for i in range(3):
            for j in range(3):
                I_totale[i][j] += M[i][j]

    return I_totale, A


def centre_geometrique(part):
    """
    Calcule le centre de masse géométrique d’un solide 3D défini par ses coordonnées [X, Y, Z]
    :param part: liste de 3 listes [X, Y, Z]
    :return: [xG, yG, zG]
    """
    X, Y, Z = part
    n = len(X)
    xG = sum(X) / n
    yG = sum(Y) / n
    zG = sum(Z) / n
    return [xG, yG, zG]


# -----------------------------------------------------------------------------------------------------------------#


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

    unit = n // 17
    n_fuselage = 4 * unit
    n_cones = 2 * unit
    n_ailes = 2 * unit
    n_empennages = 2 * unit
    n_derive = n - (n_fuselage + 2 * n_cones + 2 * n_ailes + 2 * n_empennages)

    show_debug = False
    figure_id = 2

    match figure_id:
        case 0:  # Fuselage
            part = generate_fuselage(n_fuselage)
            G = centre_geometrique(part)
            I = [[100, 0, 0], [0, 150, 0], [0, 0, 200]]
            m = 1000

        case 1:  # Aile gauche
            part = generate_trapeze_custom(n_ailes, p1=[0, 2, 0], p2=[5.5, 2, 0], p3=[2.75, 13.5, 0], p4=[0, 15, 0],
                                           epaisseur=0.5)
            G = centre_geometrique(part)
            I = [[20, 0, 0], [0, 35, 0], [0, 0, 15]]
            m = 300

        case 2:  # Aile droite
            part = generate_trapeze_custom(n_ailes, p1=[0, -2, 0], p2=[5.5, -2, 0], p3=[2.75, -13.5, 0], p4=[0, -15, 0],
                                           epaisseur=0.5)
            G = centre_geometrique(part)
            I = [[20, 0, 0], [0, 35, 0], [0, 0, 15]]
            m = 300

        case 3:  # Cône avant
            part = generate_cone(n_cones, length=6.5, R=2.0, reverse=True, offset=-13)
            G = centre_geometrique(part)
            I = [[30, 0, 0], [0, 25, 0], [0, 0, 10]]
            m = 200

        case 4:  # Cône arrière
            part = generate_cone(n_cones, length=7.0, R=2.0, reverse=False, offset=12)
            G = centre_geometrique(part)
            I = [[25, 0, 0], [0, 20, 0], [0, 0, 12]]
            m = 180

        case 5:  # Empennage gauche
            part = generate_trapeze_custom(n_ailes, p1=[-13, 2, 0], p2=[-10.5, 2, 0], p3=[-11.75, 5.5, 0],
                                           p4=[-13, 6.5, 0], epaisseur=0.5)
            G = centre_geometrique(part)
            I = [[15, 0, 0], [0, 18, 0], [0, 0, 8]]
            m = 150

        case 6:  # Dérive
            part = generate_trapeze_custom(n_cones, p1=[-13, 0, 2], p2=[-13, 0, 7], p3=[-10.25, 0, 5.75],
                                           p4=[-7.5, 0, 2], epaisseur=0.5)
            G = centre_geometrique(part)
            I = [[10, 0, 0], [0, 12, 0], [0, 0, 6]]
            m = 120

        case _:
            raise ValueError("ID de figure non reconnu (0 à 6)")

    blocs = [{"m": m, "I": I, "G": G}]
    plane = []

    part = generate_fuselage(n_fuselage)
    plane.append({
        "m": 1000,
        "I": [[100, 0, 0], [0, 150, 0], [0, 0, 200]],
        "G": centre_geometrique(part)
    })

    part = generate_cone(n_cones, length=6.5, R=2.0, reverse=True, offset=-13)
    plane.append({
        "m": 200,
        "I": [[30, 0, 0], [0, 25, 0], [0, 0, 10]],
        "G": centre_geometrique(part)
    })

    part = generate_cone(n_cones, length=7.0, R=2.0, reverse=False, offset=12)
    plane.append({
        "m": 180,
        "I": [[25, 0, 0], [0, 20, 0], [0, 0, 12]],
        "G": centre_geometrique(part)
    })

    part = generate_trapeze_custom(n_ailes, [0, 2, 0], [5.5, 2, 0], [2.75, 13.5, 0], [0, 15, 0], epaisseur=0.5)
    plane.append({
        "m": 300,
        "I": [[20, 0, 0], [0, 35, 0], [0, 0, 15]],
        "G": centre_geometrique(part)
    })

    part = generate_trapeze_custom(n_ailes, [0, -2, 0], [5.5, -2, 0], [2.75, -13.5, 0], [0, -15, 0], epaisseur=0.5)
    plane.append({
        "m": 300,
        "I": [[20, 0, 0], [0, 35, 0], [0, 0, 15]],
        "G": centre_geometrique(part)
    })

    part = generate_trapeze_custom(n_empennages, [-13, 2, 0], [-10.5, 2, 0], [-11.75, 5.5, 0], [-13, 6.5, 0],
                                   epaisseur=0.5)
    plane.append({
        "m": 150,
        "I": [[15, 0, 0], [0, 18, 0], [0, 0, 8]],
        "G": centre_geometrique(part)
    })

    part = generate_trapeze_custom(n_empennages, [-13, -2, 0], [-10.5, -2, 0], [-11.75, -5.5, 0], [-13, -6.5, 0],
                                   epaisseur=0.5)
    plane.append({
        "m": 150,
        "I": [[15, 0, 0], [0, 18, 0], [0, 0, 8]],
        "G": centre_geometrique(part)
    })

    part = generate_trapeze_custom(n_derive, [-13, 0, 2], [-13, 0, 7], [-10.25, 0, 5.75], [-7.5, 0, 2], epaisseur=0.5)
    plane.append({
        "m": 120,
        "I": [[10, 0, 0], [0, 12, 0], [0, 0, 6]],
        "G": centre_geometrique(part)
    })

    I_totale, centre_masse_global = calcul_inertie_totale(plane)

    test_bloc = blocs[0]
    G = test_bloc["G"]
    A = [coord + 3 for coord in G]

    I_moved = deplace_mat(test_bloc["I"], test_bloc["m"], G, A)
    print("Inertie déplacée vers A =", A)
    for row in I_moved:
        print(row)

    if show_debug:
        ax.scatter(*G, color='blue', s=40, label=f"G bloc {figure_id}")
        ax.text(*G, f"G{figure_id}", color='blue')

        ax.scatter(*A, color='green', s=40, label="A (point déplacé)")
        ax.text(*A, " A", color='green')

        def format_matrix(M):
            return "\n".join(["[" + ", ".join(f"{v:.1f}" for v in row) + "]" for row in M])

        text_G = f"G : I_G =\n{format_matrix(test_bloc['I'])}"
        text_A = f"A : I_A =\n{format_matrix(I_moved)}"

        ax.text(G[0], G[1], G[2] + 1, text_G, fontsize=7, color='blue')
        ax.text(A[0], A[1], A[2] + 1, text_A, fontsize=7, color='green')

        ax.plot([G[0], A[0]], [G[1], A[1]], [G[2], A[2]], color='black', linestyle='--')

        ax.scatter(*centre_masse_global, color='red', s=60, label="Centre de masse global")
        ax.text(*centre_masse_global, " A", color='red')

    print("Centre de masse global A :", centre_masse_global)
    print("Inertie totale au point A :")
    for row in I_totale:
        print(row)


    ax.legend()
    ax.grid(True)

    plt.title("Fleche pour tourner / Numpad (5123) pour se déplacer :")
    plt.show()

# -----------------------------------------------------------------------------------------------------------------#
