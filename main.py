import pygame
import sys
import logging
from menu import Menu
from grid2d import Grid2D
from toolbar import Toolbar
from block_colors import load_block_icons

# Configurar el registro
logging.basicConfig(level=logging.DEBUG)

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)  # Añade pygame.RESIZABLE
    pygame.display.set_caption("MC Builder Planner")
    clock = pygame.time.Clock()


    BLOCK_ICONS_LOADED = load_block_icons()

    menu = Menu(screen, font_size=18)
    grid2d = Grid2D(screen, grid_size=20)
    grid2d.set_icons(BLOCK_ICONS_LOADED)
    toolbar = Toolbar(screen)

    # Añadir botones a la barra de herramientas
    toolbar.add_button('assets/icons8-eraser-64.png', 'erase')
    toolbar.add_button('assets/icons8-fill-color-50.png', 'fill') 
    toolbar.add_button('assets/icons8-brush-80.png', 'brush') 
    toolbar.add_button('assets/icons8-cursor-80.png', 'cursor') 

    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()  # Obtener la posición actual del ratón
        for event in pygame.event.get():
            logging.debug(f"Evento: {event}")
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                menu.update_screen_size(screen)
                grid2d.update_screen_size(screen)
                toolbar.update_screen_size(screen)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                selected_tool = toolbar.handle_mouse_click(event)
                if selected_tool:
                    logging.debug(f"Herramienta seleccionada desde toolbar: {selected_tool}")
                if selected_tool == 'erase':
                    grid2d.selected_block = 'erase'  # Selecciona la herramienta de borrado
                    logging.debug(f"grid2d.selected_block establecido en 'erase' para borrador")
                elif selected_tool == 'fill':
                    grid2d.fill_blocks(grid2d.selected_block)  # Llama a la función fill_blocks
                elif event.button == 1:  # Clic izquierdo
                    if not menu.menu_rect.collidepoint(event.pos) and not toolbar.rect.collidepoint(event.pos):
                        if toolbar.selected_tool == 'brush':
                            grid2d.place_block(event.pos, grid2d.selected_block)
                        elif toolbar.selected_tool == 'cursor':
                            grid2d.handle_drag(event, toolbar.selected_tool)
                        elif toolbar.selected_tool == 'erase':
                            grid2d.place_block(event.pos, 'erase')
                    menu.handle_mouse_click(event)
            elif event.type == pygame.MOUSEMOTION:
                menu.handle_mouse_motion(event)
                grid2d.handle_drag(event, toolbar.selected_tool)
            elif event.type == pygame.MOUSEBUTTONUP:
                menu.handle_mouse_release(event)
                grid2d.handle_drag(event, toolbar.selected_tool)
            elif event.type == pygame.MOUSEWHEEL:
                logging.debug(f"Rueda del ratón: {event.y}, posición del ratón: {mouse_pos}")
                if menu.menu_rect.collidepoint(mouse_pos):
                    menu.handle_mouse_scroll(event)
                else:
                    grid2d.handle_zoom(event)
            elif event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                menu.handle_keypress(event)

        # Actualizar la visibilidad de la barra de herramientas
        toolbar.update_visibility(mouse_pos)

        menu.update()
        grid2d.selected_block = 'erase' if toolbar.selected_tool == 'erase' else menu.selected_block  # Actualiza el bloque seleccionado

        screen.fill((255, 255, 255))  # Color de fondo blanco
        grid2d.draw_grid()
        menu.draw()
        toolbar.draw()
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()