from OpenGL.GL import *
from OpenGL.GLU import *

def draw_cube():
    glBegin(GL_QUADS)
    # Define the vertices and draw the cube
    glEnd()

gluPerspective(45, (800/600), 0.1, 50.0)
glTranslatef(0.0, 0.0, -5)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    draw_cube()
    pygame.display.flip()
    pygame.time.wait(10)
