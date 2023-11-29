import pygame
import math
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from PIL import Image
import numpy


def load_texture(filename):
    img = Image.open(filename)
    img_data = numpy.array(list(img.getdata()), numpy.uint8)
    text_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, text_id)
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
    return text_id


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


def set_lights(directional_position, point_position, point_color):
    glEnable(GL_LIGHTING)

    # Directional light properties (left side, white)
    glLightfv(GL_LIGHT0, GL_POSITION, directional_position)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, (1.0, 1.0, 1.0, 1.0))
    glEnable(GL_LIGHT0)

    # Point light properties
    glLightfv(GL_LIGHT1, GL_POSITION, point_position)
    glLightfv(GL_LIGHT1, GL_DIFFUSE, point_color)
    glEnable(GL_LIGHT1)


def draw_pyramid(x, y, z, a, colored):
    half = a

    # bottom face
    glBegin(GL_POLYGON if colored else GL_LINE_LOOP)
    glColor3f(1, 0, 0) if colored else glColor3f(1, 0, 0)
    glVertex3f(x - half, y - half, z - half)
    glVertex3f(half + x, y - half, z - half)
    glVertex3f(half + x, y - half, z + half)
    glVertex3f(x - half, y - half, z + half)
    glEnd()

    # lines connecting bottom and top vertices
    glBegin(GL_POLYGON if colored else GL_LINE_LOOP)
    glColor3f(1, 0, 0) if colored else glColor3f(1, 0, 0)
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
    glColor3f(1, 0, 0) if colored else glColor3f(1, 0, 0)
    glVertex3f(x - half, y - half, z - half)
    glVertex3f(half + x, y - half, z - half)
    glVertex3f(x, half + y, z)
    glVertex3f(x - half, y - half, z + half)
    glEnd()


def sierpinski_pyramid(x, y, z, iterations, length, colored):
    half = length / 2

    if iterations > 1:
        sierpinski_pyramid(x - half, y - half, z - half, iterations - 1, half, colored)
        sierpinski_pyramid(x + half, y - half, z - half, iterations - 1, half, colored)
        sierpinski_pyramid(x - half, y - half, z + half, iterations - 1, half, colored)
        sierpinski_pyramid(x + half, y - half, z + half, iterations - 1, half, colored)
        sierpinski_pyramid(x, y + half, z, iterations - 1, half, colored)
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
    last_pos_x = 0
    last_pos_y = 0
    colored = [False]  # Use a list to store the coloring state
    iterations = [3]  # Use a list to store the number of iterations
    angle = 0.1

    directional_position = (-1, 0, 0, 0)
    point_position = (0, 0, 0, 1)
    point_color = (1.0, 1.0, 1.0, 1.0)

    set_lights(directional_position, point_position, point_color)

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
                if event.key == pygame.K_v:
                    colored[0] = not colored[0]
                if event.key == pygame.K_w and iterations[0] < 6:  # Increase iterations with 'w'
                    iterations[0] += 1
                if event.key == pygame.K_s and iterations[0] > 1:  # Decrease iterations with 's'
                    iterations[0] -= 1
                if event.key == pygame.K_p:  # Zmiana koloru światła na pomarańczowy
                    point_color = (1.0, 0.5, 0.0, 1.0)
                    glLightfv(GL_LIGHT1, GL_DIFFUSE, point_color)
                if event.key == pygame.K_r:  # Zmiana koloru światła na różowy
                    point_color = (1.0, 0.0, 1.0, 1.0)
                    glLightfv(GL_LIGHT1, GL_DIFFUSE, point_color)
                if event.key == pygame.K_n:  # Zmiana koloru światła na niebieski
                    point_color = (0.0, 0.0, 1.0, 1.0)
                    glLightfv(GL_LIGHT1, GL_DIFFUSE, point_color)
                if event.key == pygame.K_z:  # Zmiana koloru światła na zielony
                    point_color = (0.0, 1.0, 0.0, 1.0)
                    glLightfv(GL_LIGHT1, GL_DIFFUSE, point_color)
                if event.key == pygame.K_c:  # Zmiana koloru światła na czerwony
                    point_color = (1.0, 0.0, 0.0, 1.0)
                    glLightfv(GL_LIGHT1, GL_DIFFUSE, point_color)
                if event.key == pygame.K_f:  # Zamiana koloru światła na fiolet
                    point_color = (0.5, 0.0, 1.0, 1.0)
                    glLightfv(GL_LIGHT1, GL_DIFFUSE, point_color)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    glScaled(1.05, 1.05, 1.05)
                if event.button == 5:
                    glScaled(0.95, 0.95, 0.95)

            if event.type == pygame.MOUSEMOTION:
                x, y = event.pos
                dx = x - last_pos_x
                dy = y - last_pos_y
                mouse_state = pygame.mouse.get_pressed()
                if mouse_state[0]:
                    model_view = (GLfloat * 16)()
                    glGetFloatv(GL_MODELVIEW_MATRIX, model_view)
                    temp = (GLfloat * 3)()
                    temp[0] = model_view[0] * dy + model_view[1] * dx
                    temp[1] = model_view[4] * dy + model_view[5] * dx
                    temp[2] = model_view[8] * dy + model_view[9] * dx
                    norm_xy = math.sqrt(temp[0] * temp[0] + temp[1]
                                        * temp[1] + temp[2] * temp[2])
                    glRotatef(math.sqrt(dx * dx + dy * dy),
                              temp[0] / norm_xy, temp[1] / norm_xy, temp[2] / norm_xy)

                last_pos_x = x
                last_pos_y = y

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Draw ground
        draw_ground(70, ground_texture)

        # Draw pyramid
        glPushMatrix()
        sierpinski_pyramid(0, 0, 0, iterations[0], 2, colored[0])
        glPopMatrix()

        glRotatef(angle, 0, 1, 0)
        pygame.display.flip()
        pygame.time.wait(10)


if __name__ == "__main__":
    main()
