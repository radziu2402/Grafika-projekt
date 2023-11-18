import pygame
import math
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from PIL import Image
import numpy


def load_texture(filename):
    """
    Reads an image file and converts it to an OpenGL-readable textID format
    """
    img = Image.open(filename)
    img_data = numpy.array(list(img.getdata()), numpy.uint8)
    textID = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, textID)
    glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB,
                 img.size[0], img.size[1], 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)
    return textID


def draw_ground(size, texture_id):
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, texture_id)

    glBegin(GL_QUADS)
    glTexCoord2f(0, 0)
    glVertex3f(-size, -2, -size)
    glTexCoord2f(1, 0)
    glVertex3f(size, -2, -size)
    glTexCoord2f(1, 1)
    glVertex3f(size, -2, size)
    glTexCoord2f(0, 1)
    glVertex3f(-size, -2, size)
    glEnd()

    glDisable(GL_TEXTURE_2D)


def set_lights():
    glEnable(GL_LIGHTING)

    # Directional light properties (left side, red)
    glLightfv(GL_LIGHT0, GL_POSITION, (-1, 0, 0, 0))
    glLightfv(GL_LIGHT0, GL_DIFFUSE, (1.0, 1.0, 1.0, 1.0))
    glEnable(GL_LIGHT0)


def draw_pyramid(x, y, z, a, colored):
    half = a

    # bottom face
    glBegin(GL_POLYGON if colored else GL_LINE_LOOP)
    glColor3f(1.0, 0.5, 0.8) if colored else glColor3f(1, 0, 0)
    glVertex3f(x - half, y - half, z - half)
    glVertex3f(half + x, y - half, z - half)
    glVertex3f(half + x, y - half, z + half)
    glVertex3f(x - half, y - half, z + half)
    glEnd()

    # lines connecting bottom and top vertices
    glBegin(GL_POLYGON if colored else GL_LINE_LOOP)
    glColor3f(1.0, 0.5, 0.8) if colored else glColor3f(1, 0, 0)
    glVertex3f(x - half, y - half, z - half)
    glVertex3f(x, half + y, z)
    glVertex3f(half + x, y - half, z - half)
    glVertex3f(x, half + y, z)
    glVertex3f(half + x, y - half, z + half)
    glVertex3f(x, half + y, z)
    glVertex3f(x - half, y - half, z + half)
    glVertex3f(x, half + y, z)
    glEnd()

    # top face
    glBegin(GL_POLYGON if colored else GL_LINE_LOOP)
    glColor3f(1.0, 0.5, 0.8) if colored else glColor3f(1, 0, 0)
    glVertex3f(x - half, y - half, z - half)
    glVertex3f(half + x, y - half, z - half)
    glVertex3f(x, half + y, z)
    glVertex3f(x - half, y - half, z + half)
    glEnd()


def sierpinski_piramid(x, y, z, iterations, length, colored):
    half = length / 2

    if iterations > 1:
        sierpinski_piramid(x - half, y - half, z - half, iterations - 1, half, colored)
        sierpinski_piramid(x + half, y - half, z - half, iterations - 1, half, colored)
        sierpinski_piramid(x - half, y - half, z + half, iterations - 1, half, colored)
        sierpinski_piramid(x + half, y - half, z + half, iterations - 1, half, colored)
        sierpinski_piramid(x, y + half, z, iterations - 1, half, colored)
    else:
        draw_pyramid(x, y, z, length, colored)


def main():
    pygame.init()
    display = (1200, 800)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    pygame.key.set_repeat(200, 10)  # Increased delay between key repeats
    pygame.display.set_caption('PiramidShow')
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0, -10)
    lastPosX = 0
    lastPosY = 0
    colored = [False]  # Use a list to store the coloring state
    iterations = [3]  # Use a list to store the number of iterations
    angle = 0.1
    # set_lights()
    ground_texture = load_texture("grass.jpg")
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    glRotatef(1, 0, 1, 0)
                if event.key == pygame.K_RIGHT:
                    glRotatef(1, 0, -1, 0)
                if event.key == pygame.K_UP:
                    glRotatef(1, -1, 0, 0)
                if event.key == pygame.K_DOWN:
                    glRotatef(1, 1, 0, 0)
                if event.key == pygame.K_c:  # Toggle coloring on/off with 'c'
                    colored[0] = not colored[0]
                if event.key == pygame.K_w and iterations[0] < 6:  # Increase iterations with 'w'
                    iterations[0] += 1
                if event.key == pygame.K_s and iterations[0] > 1:  # Decrease iterations with 's'
                    iterations[0] -= 1

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    glScaled(1.05, 1.05, 1.05)
                if event.button == 5:
                    glScaled(0.95, 0.95, 0.95)

            if event.type == pygame.MOUSEMOTION:
                x, y = event.pos
                dx = x - lastPosX
                dy = y - lastPosY
                mouseState = pygame.mouse.get_pressed()
                if mouseState[0]:
                    modelView = (GLfloat * 16)()
                    glGetFloatv(GL_MODELVIEW_MATRIX, modelView)
                    temp = (GLfloat * 3)()
                    temp[0] = modelView[0] * dy + modelView[1] * dx
                    temp[1] = modelView[4] * dy + modelView[5] * dx
                    temp[2] = modelView[8] * dy + modelView[9] * dx
                    norm_xy = math.sqrt(temp[0] * temp[0] + temp[1]
                                        * temp[1] + temp[2] * temp[2])
                    glRotatef(math.sqrt(dx * dx + dy * dy),
                              temp[0] / norm_xy, temp[1] / norm_xy, temp[2] / norm_xy)

                lastPosX = x
                lastPosY = y

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Draw ground
        draw_ground(70, ground_texture)

        # Draw pyramid
        glPushMatrix()
        sierpinski_piramid(0, 0, 0, iterations[0], 2, colored[0])
        glPopMatrix()

        glRotatef(angle, 0, 1, 0)
        pygame.display.flip()
        pygame.time.wait(10)


if __name__ == "__main__":
    main()
