from Tools import *
from Vectors import Vector
import matplotlib.pyplot as plt

def rotate_point(p, axis, angle):
    v = Vector(p).rotate(axis, angle)
    return v.coords

def plot_rotated(ax, points, axis='x', angle=pi/2, **kwargs):
    rotated = [rotate_point(p, axis, angle) for p in points]
    xs = [p[0] for p in rotated]
    ys = [p[1] for p in rotated]
    zs = [p[2] for p in rotated]
    ax.plot(xs, ys, zs, **kwargs)

def generate_circle(radius, resolution):
    circle = []
    for i in range(resolution):
        theta = 2 * pi * i / resolution
        y = radius * cos(theta)
        z = radius * sin(theta)
        circle.append((y, z))
    return circle

def cylindre_plein(ax, R, h, center=(0, 0, 0), resolution=20, color='gray', alpha=0.8):
    cx, cy, cz = center
    front_circle = []
    back_circle = []

    contour = generate_circle(R, resolution)

    for y, z in contour:
        front_circle.append([cx, cy + y, cz + z])
        back_circle.append([cx + h, cy + y, cz + z])

    for i in range(resolution):
        next_i = (i + 1) % resolution
        p1 = front_circle[i]
        p2 = front_circle[next_i]
        p3 = back_circle[next_i]
        p4 = back_circle[i]
        plot_rotated(ax, [p1, p2, p3, p4, p1], color=color, alpha=alpha)

    for circle in [front_circle, back_circle]:
        plot_rotated(ax, circle + [circle[0]], color=color, alpha=alpha)

def draw_cone(ax, length, radius, center=(0, 0, 0), direction='x', reverse=False, resolution=20, color='orange', alpha=0.8):
    base = []
    for i in range(resolution):
        theta = 2 * pi * i / resolution
        y = radius * cos(theta)
        z = radius * sin(theta)
        base.append((y, z))

    for i in range(resolution):
        y1, z1 = base[i]
        y2, z2 = base[(i + 1) % resolution]

        if reverse:
            tip = (center[0] - length, center[1], center[2])
            base1 = (center[0], center[1] + y1, center[2] + z1)
            base2 = (center[0], center[1] + y2, center[2] + z2)
        else:
            tip = (center[0] + length, center[1], center[2])
            base1 = (center[0], center[1] + y1, center[2] + z1)
            base2 = (center[0], center[1] + y2, center[2] + z2)

        plot_rotated(ax, [base1, tip, base2, base1], color=color, alpha=alpha)

def draw_wing(ax, origin, span, front_length, back_length, thickness, side='right', color='darkblue'):
    x0, y0, z0 = origin
    sign = -1 if side == 'right' else 1

    # Points bas (Y = y0)
    p1 = [x0, y0, z0]  # arrière intérieur
    p2 = [x0 + back_length, y0, z0]  # avant intérieur

    # Pointe triangulaire sur même X que p1
    p3 = [x0, y0, z0 + sign * back_length ]  # pointe extérieure unique

    # Points hauts (Y = y0 + thickness)
    p5 = [p1[0], p1[1] + thickness, p1[2]]
    p6 = [p2[0], p2[1] + thickness, p2[2]]
    p7 = [p3[0], p3[1] + thickness, p3[2]]

    # Faces (triangulaires pour certaines)
    verts = [
        [p1, p2, p3],       # base inférieure
        [p5, p6, p7],       # face supérieure
        [p1, p2, p6, p5],   # intérieur (côté fuselage)
        [p2, p3, p7, p6],   # bord avant
        [p3, p1, p5, p7],   # bord arrière
    ]
    for face in verts:
        plot_rotated(ax, face + [face[0]], color=color, alpha=0.9)

def draw_wing_top(ax, origin, span, front_length, back_length, thickness, side='right', color='blue'):
    x0, y0, z0 = origin

    # Points bas (Y = y0)
    p1 = [x0, y0, z0]  # arrière intérieur
    p2 = [x0 + back_length, y0, z0]  # avant intérieur

    # Pointe triangulaire vers le haut, inverser la direction sur l'axe X
    p3 = [x0, y0 + span, z0]  # avant extérieur, sur le même X que p1 (fixé sur x0)

    # Points hauts (Y = y0 + thickness)
    p5 = [p1[0], p1[1] + thickness, p1[2]]  # haut arrière intérieur
    p6 = [p2[0], p2[1] + thickness, p2[2]]  # haut avant intérieur
    p7 = [p3[0], p3[1] + thickness, p3[2]]  # haut avant extérieur (pointe)

    verts = [
        [p1, p2, p3],       # base inférieure
        [p5, p6, p7],       # face supérieure
        [p1, p2, p6, p5],   # intérieur (côté fuselage)
        [p2, p3, p7, p6],   # bord avant
        [p3, p1, p5, p7],   # bord arrière
    ]

    for face in verts:
        plot_rotated(ax, face + [face[0]], color=color, alpha=0.9)

def renderPlane():
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    cylindre_plein(ax, R=2.0, h=39.5, center=(-19.75, 0, 0))
    draw_cone(ax, length=6.5, radius=2.0, center=(-19.75, 0, 0), direction='x', reverse=True)
    draw_cone(ax, length=7.0, radius=2.0, center=(19.75, 0, 0), direction='x')

    draw_wing(ax, origin=(0, 0, 2), span=3.0, front_length=15.0, back_length=13.5, thickness=0.5, side='left')
    draw_wing(ax, origin=(0, 0, -2), span=3.0, front_length=15.0, back_length=13.5, thickness=0.5, side='right')

    draw_wing(ax, origin=(-19.75, 0, 2), span=2.5, front_length=6.5, back_length=5.5, thickness=0.5, side='left')
    draw_wing(ax, origin=(-19.75, 0, -2), span=2.5, front_length=6.5, back_length=5.5, thickness=0.5, side='right')

    draw_wing_top(ax, origin=(-19.75, 2, 0), span=4.0, front_length=5.0, back_length=4.5, thickness=0.5)

    ax.quiver(0, 0, 0, 20, 0, 0, color='red')
    ax.quiver(0, 0, 0, 0, 20, 0, color='blue')
    ax.quiver(0, 0, 0, 0, 0, 20, color='green')

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    ax.set_box_aspect([55, 40, 10])  
    ax.set_xlim(-30, 30)
    ax.set_ylim(-25, 25) 
    ax.set_zlim(-5, 5)


    plt.tight_layout()
    plt.show()


