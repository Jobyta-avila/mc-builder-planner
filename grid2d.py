import pygame

# Define el color de las líneas de la cuadrícula
GRID_COLOR = (200, 200, 200)

def draw_grid(screen, block_size):
    width, height = screen.get_size()
    
    # Dibuja las líneas verticales
    for x in range(0, width, block_size):
        pygame.draw.line(screen, GRID_COLOR, (x, 0), (x, height))
    
    # Dibuja las líneas horizontales
    for y in range(0, height, block_size):
        pygame.draw.line(screen, GRID_COLOR, (0, y), (width, y))
