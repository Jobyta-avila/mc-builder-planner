import pygame
import sys
import logging
import pygame_menu
from menu import Menu
from grid2d import Grid2D
from toolbar import Toolbar
from block_colors import load_block_icons
from main_menu import MainMenu

# Configurar el registro
logging.basicConfig(level=logging.DEBUG)

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
    pygame.display.set_caption("MC Builder Planner")
    clock = pygame.time.Clock()

    # Menú inicial
    menu_theme = pygame_menu.themes.THEME_DARK.copy()
    menu_theme.widget_font_size = 30
    start_menu = pygame_menu.Menu('MC Builder Planner', 800, 600, theme=menu_theme)

    show_start_menu = True
    show_grid2d = False  # Variable para mostrar grid2d

    def start_2d_design():
        nonlocal show_start_menu, show_grid2d
        show_start_menu = False
        show_grid2d = True

    def exit_program():
        nonlocal running
        running = False

    start_menu.add.button('Start a 2D Design', start_2d_design)
    start_menu.add.button('Start a 3D Design', exit_program)  # Placeholder, adjust as needed
    start_menu.add.button('Exit', exit_program)

    # Cargar los iconos de bloques después de inicializar Pygame
    BLOCK_ICONS_LOADED = load_block_icons()

    main_menu = MainMenu(screen)
    menu = Menu(screen, font_size=18)  # No ajuste de posición vertical necesario
    grid2d = Grid2D(screen, grid_size=20, offset_y=40)  # Ajustar la posición vertical del grid
    grid2d.set_icons(BLOCK_ICONS_LOADED)  # Asignar los iconos cargados al grid
    toolbar = Toolbar(screen, height=60, margin_left=300)  # Ajustar la posición y tamaño del toolbar

    # Añadir botones a la barra de herramientas
    toolbar.add_button('assets/icons8-eraser-64.png', 'erase')  # Ruta relativa al icono de borrado
    toolbar.add_button('assets/icons8-fill-color-50.png', 'fill')  # Ruta relativa al icono de rellenar
    toolbar.add_button('assets/icons8-brush-80.png', 'brush')  # Ruta relativa al icono de pincel
    toolbar.add_button('assets/icons8-cursor-80.png', 'cursor')  # Ruta relativa al icono de puntero

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
                main_menu.update_screen_size(screen)
                start_menu.resize(event.w, event.h)
            if show_start_menu:
                start_menu.update(events=[event])
            elif show_grid2d:
                option = main_menu.handle_mouse_click(event)
                if option:
                    logging.debug(f"Opción del menú principal seleccionada: {option}")
                    # Agregar lógica para cada opción del menú principal aquí
                else:
                    if event.type == pygame.MOUSEBUTTONDOWN:
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
                                if toolbar.selected_tool == 'brush' or toolbar.selected_tool == 'erase':
                                    grid2d.placing_block = True
                                    grid2d.place_block(event.pos, grid2d.selected_block if toolbar.selected_tool == 'brush' else 'erase')
                                grid2d.handle_drag(event)
                            menu.handle_mouse_click(event)
                    elif event.type == pygame.MOUSEMOTION:
                        menu.handle_mouse_motion(event)
                        if (toolbar.selected_tool == 'brush' or toolbar.selected_tool == 'erase') and grid2d.placing_block:
                            grid2d.place_block(event.pos, grid2d.selected_block if toolbar.selected_tool == 'brush' else 'erase')
                        else:
                            grid2d.handle_drag(event)
                    elif event.type == pygame.MOUSEBUTTONUP:
                        menu.handle_mouse_release(event)
                        grid2d.handle_drag(event)
                        grid2d.placing_block = False
                    elif event.type == pygame.MOUSEWHEEL:
                        logging.debug(f"Rueda del ratón: {event.y}, posición del ratón: {mouse_pos}")
                        if menu.menu_rect.collidepoint(mouse_pos):
                            menu.handle_mouse_scroll(event)
                        else:
                            grid2d.handle_zoom(event)
                    elif event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                        menu.handle_keypress(event)

        screen.fill((255, 255, 255))  # Color de fondo blanco
        if show_start_menu:
            start_menu.draw(screen)
        elif show_grid2d:
            grid2d.selected_block = 'erase' if toolbar.selected_tool == 'erase' else menu.selected_block  # Actualiza el bloque seleccionado

            main_menu.draw()
            grid2d.draw_grid()
            menu.draw()
            toolbar.draw()

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()

