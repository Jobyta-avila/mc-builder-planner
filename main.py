import pygame
from grid2d import Grid2D
from menu import Menu

# Inicializa Pygame
pygame.init()

# Obtiene el tamaño de la pantalla
info = pygame.display.Info()
WIDTH, HEIGHT = 800, 600  # Tamaño por defecto para una ventana redimensionable

# Configura la pantalla para que sea redimensionable y tenga un tamaño por defecto
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption('Grid2D')

def main():
    grid = Grid2D(screen)
    menu = Menu(screen)
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # Maneja eventos del menú
            menu.handle_mouse_click(event)
            menu.handle_mouse_motion(event)
            menu.handle_keypress(event)
            menu.handle_mouse_scroll(event)
            menu.handle_mouse_release(event)

            # Solo manejar zoom y arrastre si el menú no está abierto
            if not menu.menu_open:
                grid.handle_zoom(event)
                grid.handle_drag(event)

        # Rellena la pantalla con un color de fondo blanco
        screen.fill((255, 255, 255))  # Blanco

        # Dibuja la cuadrícula
        grid.draw_grid()

        # Dibuja el menú si está abierto
        if menu.menu_open:
            menu.draw()

        # Actualiza la pantalla
        pygame.display.flip()

        # Controla los FPS
        clock.tick(30)

    pygame.quit()

if __name__ == '__main__':
    main()
