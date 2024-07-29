import pygame
import sys
from OpenGL.GL import *
from OpenGL.GLU import *

pygame.init()
screen = pygame.display.set_mode((800, 600), pygame.DOUBLEBUF | pygame.OPENGL)
pygame.display.set_caption("MC Build Planner")

gluPerspective(45, (800/600), 0.1, 50.0)
glTranslatef(0.0, 0.0, -5)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    pygame.display.flip()
    pygame.time.wait(10)
