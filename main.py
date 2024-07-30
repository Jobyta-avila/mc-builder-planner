import pygame
import sys
import logging
from menu import Menu
from grid2d import Grid2D

# Configurar el registro
logging.basicConfig(level=logging.DEBUG)

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)  # Añade pygame.RESIZABLE
    pygame.display.set_caption("Minecraft Builder Planner")
    clock = pygame.time.Clock()
    
    menu = Menu(screen, font_size=18)
    grid2d = Grid2D(screen, grid_size=20)

    running = True
    while running:
        for event in pygame.event.get():
            logging.debug(f"Evento: {event}")
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                menu.update_screen_size(screen)
                grid2d.update_screen_size(screen)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Clic izquierdo
                    if not menu.menu_rect.collidepoint(event.pos):
                        grid2d.place_block(event.pos, menu.selected_block)
                menu.handle_mouse_click(event)
            elif event.type == pygame.MOUSEMOTION:
                menu.handle_mouse_motion(event)
                grid2d.handle_drag(event)
            elif event.type == pygame.MOUSEBUTTONUP:
                menu.handle_mouse_release(event)
                grid2d.handle_drag(event)
            elif event.type == pygame.MOUSEWHEEL:
                menu.handle_mouse_scroll(event)
                grid2d.handle_zoom(event)
            elif event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                menu.handle_keypress(event)
        
        menu.update()
        grid2d.selected_block = menu.selected_block  # Actualiza el bloque seleccionado

        screen.fill((255, 255, 255))  # Color de fondo blanco
        grid2d.draw_grid()
        menu.draw()
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()


