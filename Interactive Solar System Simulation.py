from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import math
import time
import random

# -----------------------------
# WINDOW
# -----------------------------
WIDTH = 1200
HEIGHT = 800

zoom = -30
rotate_y = 0

# ⭐ CAMERA POSITION 
cam_x = 0
cam_y = 0

# ⭐ MOUSE CONTROL
mouse_down = False
last_x, last_y = 0, 0

# -----------------------------
# PLANETS
# -----------------------------
planets = [
    {"radius": 0.3, "distance": 4, "speed": 1.5, "color": (0.7, 0.7, 0.7)},
    {"radius": 0.5, "distance": 6, "speed": 1.0, "color": (0.9, 0.6, 0.1)},
    {"radius": 0.6, "distance": 8, "speed": 0.8, "color": (0.1, 0.4, 1.0)},
    {"radius": 0.45, "distance": 10, "speed": 0.6, "color": (0.8, 0.3, 0.2)}
]

# -----------------------------
# STARS
# -----------------------------
stars = [
    (random.uniform(-100, 100),
     random.uniform(-100, 100),
     random.uniform(-100, 100))
    for _ in range(500)
]

# -----------------------------
# INIT
# -----------------------------
def init():
    glEnable(GL_DEPTH_TEST)
    glShadeModel(GL_SMOOTH)

    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)

    glLightfv(GL_LIGHT0, GL_POSITION, [0, 0, 0, 1])
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [1, 1, 1, 1])

    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)

    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    glEnable(GL_FOG)
    glFogfv(GL_FOG_COLOR, [0, 0, 0, 1])
    glFogf(GL_FOG_MODE, GL_EXP2)
    glFogf(GL_FOG_DENSITY, 0.02)

    glClearColor(0, 0, 0, 1)

# -----------------------------
# ORBIT
# -----------------------------
def draw_orbit(r):
    glDisable(GL_LIGHTING)
    glColor4f(1, 1, 1, 0.15)

    glBegin(GL_LINE_LOOP)
    for i in range(360):
        a = math.radians(i)
        glVertex3f(math.cos(a)*r, 0, math.sin(a)*r)
    glEnd()

    glEnable(GL_LIGHTING)

# -----------------------------
# STARS
# -----------------------------
def draw_stars():
    glDisable(GL_LIGHTING)
    glPointSize(2)

    glBegin(GL_POINTS)
    for s in stars:
        glColor3f(1, 1, 1)
        glVertex3f(*s)
    glEnd()

    glEnable(GL_LIGHTING)

# -----------------------------
# SUN
# -----------------------------
def draw_sun():
    glDisable(GL_LIGHTING)

    for i in range(10):
        glColor4f(1.0, 0.7, 0.0, 0.08)
        glutSolidSphere(1.5 + i*0.12, 50, 50)

    glColor3f(1.0, 0.75, 0.0)
    glutSolidSphere(1.5, 60, 60)

    glEnable(GL_LIGHTING)

# -----------------------------
# PLANET
# -----------------------------
def draw_planet(p, t):
    angle = t * p["speed"]

    x = math.cos(angle) * p["distance"]
    z = math.sin(angle) * p["distance"]

    draw_orbit(p["distance"])

    glPushMatrix()
    glTranslatef(x, 0, z)

    glColor3f(*p["color"])
    glutSolidSphere(p["radius"], 40, 40)

    glPopMatrix()

# -----------------------------
# DISPLAY 
# -----------------------------
def display():
    global rotate_y

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    # ⭐ CAMERA SYSTEM 
    glTranslatef(cam_x, cam_y, zoom)

    glRotatef(20, 1, 0, 0)
    glRotatef(rotate_y, 0, 1, 0)

    t = time.time()

    draw_stars()
    draw_sun()

    for p in planets:
        draw_planet(p, t)

    glutSwapBuffers()

# -----------------------------
# RESHAPE
# -----------------------------
def reshape(w, h):
    if h == 0:
        h = 1

    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, w/h, 0.1, 500)
    glMatrixMode(GL_MODELVIEW)

# -----------------------------
# KEYBOARD (ZOOM + ROTATE + MOVE)
# -----------------------------
def keyboard(key, x, y):
    global zoom

    key = key.decode()

    if key == 'w':
        zoom += 1
    elif key == 's':
        zoom -= 1

# -----------------------------
# ARROW KEYS (CAMERA MOVE)
# -----------------------------
def special(key, x, y):
    global cam_x, cam_y, rotate_y

    if key == GLUT_KEY_UP:
        cam_y += 1
    elif key == GLUT_KEY_DOWN:
        cam_y -= 1
    elif key == GLUT_KEY_LEFT:
        cam_x -= 1
    elif key == GLUT_KEY_RIGHT:
        cam_x += 1

# -----------------------------
# MOUSE CONTROL
# -----------------------------
def mouse(button, state, x, y):
    global mouse_down, last_x, last_y

    if button == GLUT_LEFT_BUTTON:
        if state == GLUT_DOWN:
            mouse_down = True
            last_x, last_y = x, y
        else:
            mouse_down = False


def motion(x, y):
    global rotate_y, last_x, last_y

    if mouse_down:
        dx = x - last_x
        rotate_y += dx * 0.3
        last_x, last_y = x, y

# -----------------------------
# TIMER
# -----------------------------
def update(v):
    glutPostRedisplay()
    glutTimerFunc(16, update, 0)

# -----------------------------
# MAIN
# -----------------------------
def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(WIDTH, HEIGHT)
    glutCreateWindow(b"Solar System Simulation")

    init()

    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutKeyboardFunc(keyboard)
    glutSpecialFunc(special)      
    glutMouseFunc(mouse)
    glutMotionFunc(motion)
    glutTimerFunc(16, update, 0)

    glutMainLoop()

main()