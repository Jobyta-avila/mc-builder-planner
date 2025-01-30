import pygame
import logging
from block_colors import BLOCK_COLORS

class Grid2D:
    def __init__(self, screen, grid_size=20, offset_y=60):
        self.screen = screen
        self.grid_size = grid_size
        self.blocks = {}
        self.block_size = grid_size
        self.zoom_step = 5
        self.min_block_size = 10
        self.max_block_size = 100
        self.offset_x = 0
        self.offset_y = offset_y  # Adjust the offset for y position
        self.dragging = False
        self.placing_block = False  # Para saber si se está colocando un bloque
        self.last_mouse_x = 0
        self.last_mouse_y = 0
        self.selected_block = None  # Añade esto para almacenar el bloque seleccionado
        self.icons = {}
        self.scale_factor = 1  # Factor de escala inicial

    def set_icons(self, icons):
        self.icons = icons

    def update_screen_size(self, screen):
        self.screen = screen

    def draw_grid(self):
        width, height = self.screen.get_size()
        start_x = -self.offset_x % self.block_size
        start_y = -self.offset_y % self.block_size
        for x in range(start_x, width, self.block_size):
            for y in range(start_y, height, self.block_size):
                rect = pygame.Rect(x + self.offset_x, y + self.offset_y, self.block_size, self.block_size)
                pygame.draw.rect(self.screen, (200, 200, 200), rect, 1)

        for (grid_x, grid_y), block in self.blocks.items():
            screen_x = grid_x * self.block_size + self.offset_x
            screen_y = grid_y * self.block_size + self.offset_y
            icon = self.icons.get(block['type'], None)
            if icon:
                icon = pygame.transform.scale(icon, (self.block_size, self.block_size))
                self.screen.blit(icon, (screen_x, screen_y))
            else:
                pygame.draw.rect(self.screen, block['color'], (screen_x, screen_y, self.block_size, self.block_size))

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
            old_block_size = self.block_size
            if event.y > 0:  # Rueda del ratón hacia arriba (zoom in)
                self.block_size += self.zoom_step
                if self.block_size > self.max_block_size:
                    self.block_size = self.max_block_size
            elif event.y < 0:  # Rueda del ratón hacia abajo (zoom out)
                self.block_size -= self.zoom_step
                if self.block_size < self.min_block_size:
                    self.block_size = self.min_block_size

            scale_factor = self.block_size / old_block_size

            # Ajustar las posiciones de los bloques existentes
            updated_blocks = {}
            for (grid_x, grid_y), block in self.blocks.items():
                new_x = int(grid_x * scale_factor)
                new_y = int(grid_y * scale_factor)
                updated_blocks[(new_x, new_y)] = block
            self.blocks = updated_blocks

            logging.debug(f"Zoom: nuevo tamaño de bloque {self.block_size}")

    def handle_drag(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Botón izquierdo del ratón
                self.dragging = True
                self.last_mouse_x, self.last_mouse_y = event.pos
                logging.debug("Iniciado arrastre")
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Botón izquierdo del ratón
                self.dragging = False
                self.placing_block = False
                logging.debug("Finalizado arrastre")
        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                dx = event.pos[0] - self.last_mouse_x
                dy = event.pos[1] - self.last_mouse_y
                new_offset_x = self.offset_x + dx
                new_offset_y = self.offset_y + dy

                if self.blocks:
                    # Obtener el tamaño del grid en bloques
                    grid_width = max(self.blocks.keys(), key=lambda k: k[0])[0] * self.block_size
                    grid_height = max(self.blocks.keys(), key=lambda k: k[1])[1] * self.block_size

                    # Limitar el movimiento de la cuadrícula para no sobrepasar el main_menu y el toolbar
                    max_offset_x = min(0, self.screen.get_width() - grid_width)
                    max_offset_y = min(0, self.screen.get_height() - grid_height)

                    if new_offset_x > 0:
                        new_offset_x = 0
                    if new_offset_y > 0:
                        new_offset_y = 0
                    if new_offset_x < max_offset_x:
                        new_offset_x = max_offset_x
                    if new_offset_y < max_offset_y:
                        new_offset_y = max_offset_y

                self.offset_x = new_offset_x
                self.offset_y = new_offset_y

                self.last_mouse_x, self.last_mouse_y = event.pos
                logging.debug(f"Arrastre de cuadrícula a offset ({self.offset_x}, {self.offset_y})")
            elif self.placing_block:
                self.place_block(event.pos, self.selected_block if self.selected_block != 'erase' else 'erase')

    def update(self, event, menu_rect, toolbar_rect, tool):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if not menu_rect.collidepoint(event.pos) and not toolbar_rect.collidepoint(event.pos):
                if tool == 'brush' or tool == 'erase':
                    self.placing_block = True
                    self.place_block(event.pos, self.selected_block if tool == 'brush' else 'erase')
        self.handle_zoom(event)
        self.handle_drag(event)
