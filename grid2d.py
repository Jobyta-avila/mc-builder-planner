import pygame
import logging
from block_colors import BLOCK_COLORS

class Grid2D:
    def __init__(self, screen, grid_size=20, offset_y=0):
        self.screen = screen
        self.grid_size = grid_size
        self.blocks = {}
        self.block_size = grid_size
        self.zoom_step = 5
        self.min_block_size = 10
        self.max_block_size = 100
        self.offset_y = offset_y
        self.offset_x = 0
        self.offset_y = 0
        self.dragging = False
        self.placing_block = False  # Para saber si se está colocando un bloque
        self.last_mouse_x = 0
        self.last_mouse_y = 0
        self.selected_block = None  # Añade esto para almacenar el bloque seleccionado
        self.icons = {}
        self.dragging_scrollbar_x = False
        self.dragging_scrollbar_y = False

        # Crear barras de desplazamiento
        self.scrollbar_width = 15
        self.scrollbar_color = (180, 180, 180)
        self.scrollbar_handle_color = (150, 150, 150)
        self.scrollbar_rect_x = pygame.Rect(0, screen.get_height() - self.scrollbar_width, screen.get_width() - self.scrollbar_width, self.scrollbar_width)
        self.scrollbar_rect_y = pygame.Rect(screen.get_width() - self.scrollbar_width, 0, self.scrollbar_width, screen.get_height() - self.scrollbar_width)
        self.scrollbar_handle_x = pygame.Rect(0, screen.get_height() - self.scrollbar_width, 30, self.scrollbar_width)
        self.scrollbar_handle_y = pygame.Rect(screen.get_width() - self.scrollbar_width, 0, self.scrollbar_width, 30)
        self.set_initial_scrollbar_position()
        self.update_scrollbars()

    def set_icons(self, icons):
        self.icons = icons

    def update_screen_size(self, screen):
        self.screen = screen
        self.update_scrollbars()

    def set_initial_scrollbar_position(self):
        """Set the initial position of the scrollbars to the center of the grid."""
        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()
        total_grid_width = screen_width // self.min_block_size * self.block_size
        total_grid_height = screen_height // self.min_block_size * self.block_size

        self.offset_x = (total_grid_width - screen_width) // 2
        self.offset_y = (total_grid_height - screen_height) // 2
        self.scrollbar_handle_x.x = self.scrollbar_rect_x.width // 2 - self.scrollbar_handle_x.width // 2
        self.scrollbar_handle_y.y = self.scrollbar_rect_y.height // 2 - self.scrollbar_handle_y.height // 2

    def update_scrollbars(self):
        visible_width = self.screen.get_width() // self.block_size
        total_width = (self.screen.get_width() // self.min_block_size) * self.block_size
        visible_height = self.screen.get_height() // self.block_size
        total_height = (self.screen.get_height() // self.min_block_size) * self.block_size

        self.scrollbar_rect_x.width = self.screen.get_width() - self.scrollbar_width
        self.scrollbar_rect_x.y = self.screen.get_height() - self.scrollbar_width
        self.scrollbar_handle_x.width = max(self.screen.get_width() * (visible_width / total_width), 30)
        self.scrollbar_handle_x.y = self.screen.get_height() - self.scrollbar_width
        self.scrollbar_handle_x.x = self.offset_x * (self.scrollbar_rect_x.width / total_width)

        self.scrollbar_rect_y.height = self.screen.get_height() - self.scrollbar_width
        self.scrollbar_rect_y.x = self.screen.get_width() - self.scrollbar_width
        self.scrollbar_handle_y.height = max(self.screen.get_height() * (visible_height / total_height), 30)
        self.scrollbar_handle_y.x = self.screen.get_width() - self.scrollbar_width
        self.scrollbar_handle_y.y = self.offset_y * (self.scrollbar_rect_y.height / total_height)

    def draw_grid(self):
        width, height = self.screen.get_size()
        for x in range(0, width, self.grid_size):
            for y in range(self.offset_y, height, self.grid_size):
                rect = pygame.Rect(x, y, self.grid_size, self.grid_size)
                pygame.draw.rect(self.screen, (200, 200, 200), rect, 1)

        for (x, y), block in self.blocks.items():
            icon = self.icons.get(block['type'], None)
            if icon:
                icon = pygame.transform.scale(icon, (self.grid_size, self.grid_size))
                self.screen.blit(icon, (x * self.grid_size + self.offset_x, y * self.grid_size + self.offset_y))
            else:
                pygame.draw.rect(self.screen, block['color'], (x * self.grid_size + self.offset_x, y * self.grid_size + self.offset_y, self.grid_size, self.grid_size))

        # Dibujar barras de desplazamiento
        pygame.draw.rect(self.screen, self.scrollbar_color, self.scrollbar_rect_x)
        pygame.draw.rect(self.screen, self.scrollbar_color, self.scrollbar_rect_y)
        pygame.draw.rect(self.screen, self.scrollbar_handle_color, self.scrollbar_handle_x)
        pygame.draw.rect(self.screen, self.scrollbar_handle_color, self.scrollbar_handle_y)

    def place_block(self, pos, block_type):
        x, y = pos
        grid_x = (x - self.offset_x) // self.block_size
        grid_y = (y - self.offset_y) // self.block_size
        if block_type == 'erase':
            if (grid_x, grid_y) in self.blocks:
                del self.blocks[(grid_x, grid_y)]
                logging.debug(f"Bloque en ({grid_x}, {grid_y}) eliminado")
        else:
            if block_type in self.icons:
                self.blocks[(grid_x, grid_y)] = {'type': block_type, 'icon': self.icons[block_type]}
                logging.debug(f"Icono del bloque en ({grid_x}, {grid_y}) actualizado con tipo {block_type}")
            else:
                block_color = BLOCK_COLORS.get(block_type, (255, 255, 255))  # Usa el color del bloque o blanco por defecto
                self.blocks[(grid_x, grid_y)] = {'type': block_type, 'color': block_color}
                logging.debug(f"Bloque en ({grid_x}, {grid_y}) actualizado con tipo {block_type}")

    def fill_blocks(self, block_type):
        width, height = self.screen.get_size()
        for x in range(self.offset_x % self.block_size, width, self.block_size):
            for y in range(self.offset_y % self.block_size, height, self.block_size):
                grid_x = x // self.block_size
                grid_y = y // self.block_size
                if block_type in self.icons:
                    self.blocks[(grid_x, grid_y)] = {'type': block_type, 'icon': self.icons[block_type]}
                    logging.debug(f"Icono del bloque en ({grid_x}, {grid_y}) actualizado con tipo {block_type}")
                else:
                    block_color = BLOCK_COLORS.get(block_type, (255, 255, 255))
                    self.blocks[(grid_x, grid_y)] = {'type': block_type, 'color': block_color}
                    logging.debug(f"Bloque en ({grid_x}, {grid_y}) actualizado con tipo {block_type}")

    def handle_zoom(self, event):
        if event.type == pygame.MOUSEWHEEL:
            logging.debug(f"Zoom de la cuadrícula: {event.y}")
            if event.y > 0:  # Rueda del ratón hacia arriba (zoom in)
                self.block_size += self.zoom_step
                if self.block_size > self.max_block_size:
                    self.block_size = self.max_block_size
            elif event.y < 0:  # Rueda del ratón hacia abajo (zoom out)
                self.block_size -= self.zoom_step
                if self.block_size < self.min_block_size:
                    self.block_size = self.min_block_size
            self.update_scrollbars()  # Actualizar barras de desplazamiento en cada cambio de zoom
            logging.debug(f"Zoom: nuevo tamaño de bloque {self.block_size}")

    def handle_drag(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Botón izquierdo del ratón
                self.dragging = True
                self.last_mouse_x, self.last_mouse_y = event.pos
                if self.scrollbar_handle_x.collidepoint(event.pos):
                    self.dragging_scrollbar_x = True
                elif self.scrollbar_handle_y.collidepoint(event.pos):
                    self.dragging_scrollbar_y = True
                logging.debug("Iniciado arrastre")
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Botón izquierdo del ratón
                self.dragging = False
                self.placing_block = False
                self.dragging_scrollbar_x = False
                self.dragging_scrollbar_y = False
                logging.debug("Finalizado arrastre")
        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                if self.placing_block:
                    self.place_block(event.pos, self.selected_block if self.selected_block != 'erase' else 'erase')
                elif self.dragging_scrollbar_x:
                    dx = event.pos[0] - self.last_mouse_x
                    self.offset_x += dx  # Invertir la dirección
                    self.last_mouse_x = event.pos[0]
                    self.update_scrollbars()
                    logging.debug(f"Arrastre de barra de desplazamiento horizontal a offset ({self.offset_x}, {self.offset_y})")
                elif self.dragging_scrollbar_y:
                    dy = event.pos[1] - self.last_mouse_y
                    self.offset_y += dy  # Invertir la dirección
                    self.last_mouse_y = event.pos[1]
                    self.update_scrollbars()
                    logging.debug(f"Arrastre de barra de desplazamiento vertical a offset ({self.offset_x}, {self.offset_y})")
                else:
                    dx = event.pos[0] - self.last_mouse_x
                    dy = event.pos[1] - self.last_mouse_y
                    self.offset_x += dx
                    self.offset_y += dy
                    self.last_mouse_x, self.last_mouse_y = event.pos
                    self.update_scrollbars()
                    logging.debug(f"Arrastre de cuadrícula a offset ({self.offset_x}, {self.offset_y})")

    def update(self, event, menu_rect, toolbar_rect, tool):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if not menu_rect.collidepoint(event.pos) and not toolbar_rect.collidepoint(event.pos):
                if tool == 'brush' or tool == 'erase':
                    self.placing_block = True
                    self.place_block(event.pos, self.selected_block if tool == 'brush' else 'erase')
        self.handle_zoom(event)
        self.handle_drag(event)




