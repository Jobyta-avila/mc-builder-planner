import pygame
from grid2d import draw_grid
from viewer3d import draw_cube
from terrain import Terrain

def run_app():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Minecraft Planner")
    clock = pygame.time.Clock()
    
    terrain = Terrain(100, 100)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        screen.fill((255, 255, 255))
        draw_grid(screen)
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
