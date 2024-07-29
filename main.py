import pygame
from grid2d import Grid2D
from menu import Menu

# Inicializa Pygame
pygame.init()



# Configura la pantalla para que sea redimensionable y tenga un tamaño por defecto

pygame.display.set_caption('Minecraft Build Planner')

def main():

    # Obtiene el tamaño de la pantalla
    info = pygame.display.Info()
    WIDTH, HEIGHT = 800, 600  # Tamaño por defecto para una ventana redimensionable
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)

    # Inicializa la cuadrícula y el menú
    grid = Grid2D(screen)
    menu = Menu(screen)
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.VIDEORESIZE:
                # Actualiza la pantalla y las dimensiones del menú y la cuadrícula
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                grid.update_screen_size(screen)
                menu.update_menu_rect()

            # Manejar eventos para la cuadrícula y el menú
            grid.update(event)
            menu.handle_mouse_motion(event)
            menu.handle_mouse_click(event)
            menu.handle_mouse_release(event)
            menu.handle_mouse_scroll(event)
            menu.handle_keypress(event)

        # Rellena la pantalla con el fondo blanco
        screen.fill((255, 255, 255))

        # Dibuja la cuadrícula
        grid.draw_grid()

        # Dibuja el menú
        menu.draw()

        # Actualiza la pantalla
        pygame.display.flip()

        # Controla los FPS
        clock.tick(30)

    pygame.quit()

if __name__ == '__main__':
    main()
