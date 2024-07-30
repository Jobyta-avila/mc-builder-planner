import pygame
import pygame.freetype  # Para fuentes de texto más avanzadas
import time
import logging
from block_colors import BLOCK_COLORS  # Importa el diccionario de colores

MENU_COLOR = (200, 200, 200)  # Gris claro
TEXT_COLOR = (0, 0, 0)  # Negro
INPUT_COLOR = (255, 255, 255)  # Blanco
INPUT_BORDER_COLOR = (0, 0, 0)  # Negro
SCROLL_BAR_COLOR = (150, 150, 150)  # Gris medio
PLACEHOLDER_COLOR = (180, 180, 180)  # Gris claro para el texto del indicador
SELECTED_COLOR = (255, 0, 0)  # Rojo para indicar el bloque seleccionado

# Definir las categorías y los bloques
CATEGORIES = {
    "Building Blocks": [
        'Stone', 'Granite', 'Polished Granite', 'Diorite', 'Polished Diorite',
        'Andesite', 'Polished Andesite', 'Deepslate', 'Cobbled Deepslate',
        'Polished Deepslate', 'Calcite', 'Tuff', 'Dripstone Block', 'Grass Block',
        'Dirt', 'Coarse Dirt', 'Podzol', 'Rooted Dirt', 'Mud', 'Crimson Nylium',
        'Warped Nylium', 'Cobblestone', 'Sand', 'Red Sand', 'Gravel', 'Sandstone',
        'Red Sandstone', 'Prismarine', 'Prismarine Bricks', 'Dark Prismarine',
        'Netherrack', 'Basalt', 'Polished Basalt', 'Smooth Basalt', 'Soul Soil',
        'End Stone', 'End Stone Bricks', 'Purpur Block', 'Purpur Pillar',
        'Purpur Stairs', 'Purpur Slab'
    ],
    "Wood": [
        'Oak Log', 'Spruce Log', 'Birch Log', 'Jungle Log', 'Acacia Log',
        'Dark Oak Log', 'Mangrove Log', 'Bamboo Block', 'Crimson Stem',
        'Warped Stem', 'Stripped Oak Log', 'Stripped Spruce Log',
        'Stripped Birch Log', 'Stripped Jungle Log', 'Stripped Acacia Log',
        'Stripped Dark Oak Log', 'Stripped Mangrove Log', 'Stripped Bamboo Block',
        'Stripped Crimson Stem', 'Stripped Warped Stem', 'Oak Planks',
        'Spruce Planks', 'Birch Planks', 'Jungle Planks', 'Acacia Planks',
        'Dark Oak Planks', 'Mangrove Planks', 'Bamboo Planks', 'Crimson Planks',
        'Warped Planks'
    ]
    # Añade más categorías aquí...
}

class Menu:
    def __init__(self, screen, font_size=24):
        self.screen = screen
        self.font = pygame.freetype.SysFont(None, font_size)
        self.menu_width = 300
        self.menu_open = False
        self.menu_rect = pygame.Rect(0, 0, self.menu_width, screen.get_height())
        self.input_box = pygame.Rect(10, 10, self.menu_width - 20, 30)
        self.input_box_active = False
        self.text = ''
        self.filtered_blocks = CATEGORIES  # Inicializar con categorías
        self.scroll_offset = 0
        self.scroll_speed = 20
        self.scrollbar_width = 10
        self.dragging_scrollbar = False
        self.scrollbar_start_y = 0
        self.last_backspace_time = 0
        self.backspace_delay = 0.05  # Tiempo de espera entre eliminaciones de caracteres
        self.backspace_held = False
        self.selected_block = None
        self.selected_block_rect = None
        self.update_menu_rect()

    def update_screen_size(self, screen):
        self.screen = screen
        self.update_menu_rect()

    def update_menu_rect(self):
        self.menu_rect = pygame.Rect(0, 0, self.menu_width, self.screen.get_height())
        self.input_box = pygame.Rect(10, 10, self.menu_width - 20, 30)

    def draw(self):
        if self.menu_open:
            pygame.draw.rect(self.screen, MENU_COLOR, self.menu_rect)
            pygame.draw.rect(self.screen, INPUT_COLOR, self.input_box)
            pygame.draw.rect(self.screen, INPUT_BORDER_COLOR, self.input_box, 2)
            
            if self.input_box_active and self.text == '':
                self.font.render_to(self.screen, (self.input_box.x + 5, self.input_box.y + 5), "Type to search...", PLACEHOLDER_COLOR)
            else:
                self.font.render_to(self.screen, (self.input_box.x + 5, self.input_box.y + 5), self.text, TEXT_COLOR)
            
            total_list_height = sum(len(blocks) for blocks in self.filtered_blocks.values()) * (self.font.get_sized_height() + 2)
            visible_height = self.menu_rect.height - self.input_box.height - 40
            if total_list_height > 0:
                scrollbar_height = max(20, visible_height * visible_height // total_list_height)
                scrollbar_position = (self.scroll_offset * (visible_height - scrollbar_height)) // max(1, total_list_height - visible_height)
                self.scrollbar_rect = pygame.Rect(self.menu_rect.width - self.scrollbar_width, self.input_box.height + 20 + scrollbar_position, self.scrollbar_width, scrollbar_height)
                pygame.draw.rect(self.screen, SCROLL_BAR_COLOR, self.scrollbar_rect)
            else:
                self.scrollbar_rect = pygame.Rect(self.menu_rect.width - self.scrollbar_width, self.input_box.height + 20, self.scrollbar_width, visible_height)

            y = self.input_box.bottom + 10
            for category, blocks in self.filtered_blocks.items():
                self.font.render_to(self.screen, (10, y - self.scroll_offset), category, TEXT_COLOR)
                y += self.font.get_sized_height() + 2
                for block in blocks:
                    block_rect = pygame.Rect(20, y - self.scroll_offset, self.menu_width - 40, self.font.get_sized_height() + 2)
                    if self.selected_block == block:
                        pygame.draw.rect(self.screen, SELECTED_COLOR, block_rect)
                    block_color = BLOCK_COLORS.get(block, TEXT_COLOR)  # Usa el color del bloque o el color de texto por defecto si no se encuentra
                    self.font.render_to(self.screen, (30, y - self.scroll_offset), block, block_color)
                    y += self.font.get_sized_height() + 2

    def handle_mouse_motion(self, event):
        if event.type == pygame.MOUSEMOTION:
            if self.dragging_scrollbar:
                mouse_y = event.pos[1]
                dy = mouse_y - self.scrollbar_start_y
                self.scrollbar_start_y = mouse_y
                total_list_height = sum(len(blocks) for blocks in self.filtered_blocks.values()) * (self.font.get_sized_height() + 2)
                visible_height = self.menu_rect.height - self.input_box.height - 40
                max_scroll_offset = max(0, total_list_height - visible_height)
                self.scroll_offset = min(max(0, self.scroll_offset + dy * (total_list_height / visible_height)), max_scroll_offset)
            else:
                if self.menu_rect.collidepoint(event.pos):
                    self.menu_open = True
                else:
                    self.menu_open = False

    def handle_mouse_click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.menu_open:
                if self.input_box.collidepoint(event.pos):
                    self.input_box_active = True
                else:
                    self.input_box_active = False
                if self.scrollbar_rect and self.scrollbar_rect.collidepoint(event.pos):
                    self.dragging_scrollbar = True
                    self.scrollbar_start_y = event.pos[1]
                else:
                    self.select_block(event.pos)
                logging.debug(f"Click en {event.pos} - Bloque seleccionado: {self.selected_block}")

    def handle_mouse_release(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            self.dragging_scrollbar = False

    def handle_mouse_scroll(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.menu_open and event.button == 4:  # Rueda hacia arriba
                self.scroll_offset = max(0, self.scroll_offset - self.scroll_speed)
            elif self.menu_open and event.button == 5:  # Rueda hacia abajo
                total_list_height = sum(len(blocks) for blocks in self.filtered_blocks.values()) * (self.font.get_sized_height() + 2)
                max_scroll_offset = max(0, total_list_height - (self.menu_rect.height - self.input_box.height - 40))
                self.scroll_offset = min(max_scroll_offset, self.scroll_offset + self.scroll_speed)

    def handle_keypress(self, event):
        if event.type == pygame.KEYDOWN and self.input_box_active:
            if event.key == pygame.K_BACKSPACE:
                self.backspace_held = True
                current_time = time.time()
                if current_time - self.last_backspace_time >= self.backspace_delay:
                    self.text = self.text[:-1]
                    self.filter_blocks()
                    self.last_backspace_time = current_time
            elif event.key == pygame.K_RETURN:
                self.filter_blocks()
            else:
                self.text += event.unicode
                self.filter_blocks()
        elif event.type == pygame.KEYUP and event.key == pygame.K_BACKSPACE:
            self.backspace_held = False

    def update(self):
        if self.backspace_held:
            current_time = time.time()
            if current_time - self.last_backspace_time >= self.backspace_delay:
                self.text = self.text[:-1]
                self.filter_blocks()
                self.last_backspace_time = current_time

    def filter_blocks(self):
        self.filtered_blocks = {
            category: [block for block in blocks if self.text.lower() in block.lower()]
            for category, blocks in CATEGORIES.items()
        }
        if self.text == '':
            self.filtered_blocks = CATEGORIES

    def select_block(self, mouse_pos):
        y = self.input_box.bottom + 10 - self.scroll_offset
        for category, blocks in self.filtered_blocks.items():
            y += self.font.get_sized_height() + 2
            for block in blocks:
                block_rect = pygame.Rect(20, y, self.menu_width - 40, self.font.get_sized_height() + 2)
                if block_rect.collidepoint(mouse_pos):
                    self.selected_block = block
                    self.selected_block_rect = block_rect
                    logging.debug(f"Bloque seleccionado: {self.selected_block}")
                    return
                y += self.font.get_sized_height() + 2

