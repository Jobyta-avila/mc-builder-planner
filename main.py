import pygame
from grid2d import draw_grid

# Inicializa Pygame
pygame.init()

# Configura la pantalla
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Grid2D')

BLOCK_SIZE = 20

def main():
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Rellena la pantalla con un color de fondo
        screen.fill((0, 0, 0))

        # Dibuja la cuadrícula
        draw_grid(screen, BLOCK_SIZE)

        # Actualiza la pantalla
        pygame.display.flip()

        # Controla los FPS
        clock.tick(30)

    pygame.quit()

if __name__ == '__main__':
    main()
