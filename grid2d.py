import pygame
import logging
from block_colors import BLOCK_COLORS  # Importa el diccionario de colores

GRID_COLOR = (0, 0, 0)  # Negro
SELECTED_COLOR = (255, 0, 0)  # Rojo para indicar el bloque seleccionado por defecto
ERASE_COLOR = (255, 255, 255)  # Blanco para borrar bloques

class Grid2D:
    def __init__(self, screen, grid_size=20):
        self.screen = screen
        self.grid_size = grid_size
        self.blocks = {}
        self.block_size = grid_size
        self.zoom_step = 5
        self.min_block_size = 10
        self.max_block_size = 100
        self.offset_x = 0
        self.offset_y = 0
        self.dragging = False
        self.placing_block = False  # Para saber si se está colocando un bloque
        self.last_mouse_x = 0
        self.last_mouse_y = 0
        self.selected_block = None  # Añade esto para almacenar el bloque seleccionado

    def update_screen_size(self, screen):
        self.screen = screen

    def draw_grid(self):
        width, height = self.screen.get_size()
        for x in range(self.offset_x % self.block_size, width, self.block_size):
            for y in range(self.offset_y % self.block_size, height, self.block_size):
                rect = pygame.Rect(x, y, self.block_size, self.block_size)
                pygame.draw.rect(self.screen, (200, 200, 200), rect, 1)

        for (x, y), block in self.blocks.items():
            pygame.draw.rect(self.screen, block['color'], (x * self.block_size + self.offset_x, y * self.block_size + self.offset_y, self.block_size, self.block_size))

    def place_block(self, pos, block_type):
        x, y = pos
        grid_x = (x - self.offset_x) // self.block_size
        grid_y = (y - self.offset_y) // self.block_size
        if block_type == 'erase':
            if (grid_x, grid_y) in self.blocks:
                del self.blocks[(grid_x, grid_y)]
                logging.debug(f"Bloque en ({grid_x}, {grid_y}) eliminado")
        else:
            block_color = BLOCK_COLORS.get(block_type, SELECTED_COLOR)  # Usa el color del bloque o el color seleccionado por defecto
            self.blocks[(grid_x, grid_y)] = {'type': block_type, 'color': block_color}
            logging.debug(f"Bloque en ({grid_x}, {grid_y}) actualizado con color {block_color}")

    def fill_blocks(self, block_type):
        block_color = BLOCK_COLORS.get(block_type, SELECTED_COLOR)
        width, height = self.screen.get_size()
        for x in range(self.offset_x % self.block_size, width, self.block_size):
            for y in range(self.offset_y % self.block_size, height, self.block_size):
                grid_x = x // self.block_size
                grid_y = y // self.block_size
                self.blocks[(grid_x, grid_y)] = {'type': block_type, 'color': block_color}
        logging.debug(f"Rellenado completo con color {block_color}")

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
            logging.debug(f"Zoom: nuevo tamaño de bloque {self.block_size}")

    def handle_drag(self, event, tool):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Botón izquierdo del ratón
                self.dragging = True
                self.last_mouse_x, self.last_mouse_y = event.pos
                if tool == 'brush' or tool == 'erase':
                    self.placing_block = True
                    self.place_block(event.pos, self.selected_block if tool == 'brush' else 'erase')
                logging.debug("Iniciado arrastre")
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Botón izquierdo del ratón
                self.dragging = False
                self.placing_block = False
                logging.debug("Finalizado arrastre")
        elif event.type == pygame.MOUSEMOTION:
            if self.dragging and self.placing_block:
                self.place_block(event.pos, self.selected_block if tool == 'brush' else 'erase')
            elif self.dragging and tool == 'cursor':
                dx = event.pos[0] - self.last_mouse_x
                dy = event.pos[1] - self.last_mouse_y
                self.offset_x += dx
                self.offset_y += dy
                self.last_mouse_x, self.last_mouse_y = event.pos
                logging.debug(f"Arrastre de cuadrícula a offset ({self.offset_x}, {self.offset_y})")

    def update(self, event, menu_rect, toolbar_rect, tool):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if not menu_rect.collidepoint(event.pos) and not toolbar_rect.collidepoint(event.pos):
                if tool == 'brush':
                    self.placing_block = True
                    self.place_block(event.pos, self.selected_block)
                elif tool == 'erase':
                    self.placing_block = True
                    self.place_block(event.pos, 'erase')
        self.handle_zoom(event)
        self.handle_drag(event, tool)

