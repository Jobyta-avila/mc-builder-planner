import pygame
import pygame.freetype  # Para fuentes de texto más avanzadas

MENU_COLOR = (200, 200, 200)  # Gris claro
TEXT_COLOR = (0, 0, 0)  # Negro
INPUT_COLOR = (255, 255, 255)  # Blanco
INPUT_BORDER_COLOR = (0, 0, 0)  # Negro
SCROLL_BAR_COLOR = (150, 150, 150)  # Gris medio

# Lista de bloques en orden alfabético
BLOCK_LIST = [
    'Activator Rail', 'Air', 'Allow and Deny', 'Amethyst Cluster', 'An Ant',
    # (Añade el resto de bloques aquí)
]

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.menu_width = 300
        self.menu_open = False
        self.font = pygame.font.SysFont(None, 18)
        self.input_font = pygame.freetype.SysFont(None, 20)
        self.input_box = pygame.Rect(10, 10, self.menu_width - 20, 30)
        self.text = ''
        self.filtered_blocks = BLOCK_LIST[:]  # Inicializa con la lista completa de bloques
        self.scroll_offset = 0
        self.scroll_speed = 10
        self.dragging_scrollbar = False
        self.scrollbar_start_y = 0
        self.back_button_rect = None
        self.update_menu_rect()  # Asegúrate de llamar a este método después de inicializar los atributos

    def update_menu_rect(self):
        self.menu_rect = pygame.Rect(0, 0, self.menu_width, self.screen.get_height())
        self.input_box = pygame.Rect(10, 10, self.menu_width - 20, 30)
        self.max_visible_blocks = self.calculate_max_visible_blocks()
        self.scrollbar_rect = self.draw_scroll_bar()

    def calculate_max_visible_blocks(self):
        return (self.menu_rect.height - self.input_box.height - 20) // (self.font.get_height() + 2)

    def draw(self):
        if not self.menu_open:
            return
        
        pygame.draw.rect(self.screen, MENU_COLOR, self.menu_rect)
        self.draw_input_box()
        self.draw_block_list()
        self.draw_scroll_bar()
        self.draw_back_button()

    def draw_input_box(self):
        pygame.draw.rect(self.screen, INPUT_COLOR, self.input_box)
        pygame.draw.rect(self.screen, INPUT_BORDER_COLOR, self.input_box, 2)
        txt_surface, _ = self.input_font.render(self.text, TEXT_COLOR)
        self.screen.blit(txt_surface, (self.input_box.x + 5, self.input_box.y + 5))

    def draw_block_list(self):
        total_list_height = len(self.filtered_blocks) * (self.font.get_height() + 2)
        max_scroll_offset = max(0, total_list_height - (self.menu_rect.height - self.input_box.height - 40))
        self.scroll_offset = min(self.scroll_offset, max_scroll_offset)

        y_offset = self.input_box.bottom + 10 - self.scroll_offset
        start_index = int(self.scroll_offset // (self.font.get_height() + 2))
        end_index = int(start_index + self.max_visible_blocks)
        blocks_to_draw = self.filtered_blocks[start_index:end_index]

        for block in blocks_to_draw:
            text = self.font.render(block, True, TEXT_COLOR)
            self.screen.blit(text, (10, y_offset))
            y_offset += self.font.get_height() + 2

    def draw_scroll_bar(self):
        total_list_height = len(self.filtered_blocks) * (self.font.get_height() + 2)
        if total_list_height <= self.menu_rect.height - self.input_box.height - 40:
            return pygame.Rect(0, 0, 0, 0)  # No dibuja la barra si no es necesaria

        scrollbar_height = max(30, self.menu_rect.height * ((self.menu_rect.height - self.input_box.height - 40) / total_list_height))
        scrollbar_y = self.input_box.bottom + 10 + (self.scroll_offset * (self.menu_rect.height - self.input_box.height - 40 - scrollbar_height) / max(1, total_list_height - (self.menu_rect.height - self.input_box.height - 40)))
        scrollbar_rect = pygame.Rect(self.menu_rect.width - 10, scrollbar_y, 10, scrollbar_height)

        pygame.draw.rect(self.screen, SCROLL_BAR_COLOR, scrollbar_rect)
        return scrollbar_rect
    
    def draw_back_button(self):
        if self.back_button_rect is None:
            self.back_button_rect = pygame.Rect(10, self.menu_rect.height - 40, self.menu_width - 20, 30)
        pygame.draw.rect(self.screen, (150, 0, 0), self.back_button_rect)
        back_text = self.font.render('Back', True, TEXT_COLOR)
        self.screen.blit(back_text, (self.back_button_rect.x + 10, self.back_button_rect.y + 5))

    def handle_mouse_motion(self, event):
        if event.type == pygame.MOUSEMOTION:
            print(f"Mouse moved to {event.pos}")
            if self.menu_open and self.scrollbar_rect and self.scrollbar_rect.collidepoint(event.pos):
                print("Mouse is over the scrollbar")
                self.dragging_scrollbar = True
                self.scrollbar_start_y = event.pos[1]

    def handle_mouse_click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.menu_open:
                if self.back_button_rect and self.back_button_rect.collidepoint(event.pos):
                    self.menu_open = False
                elif self.input_box.collidepoint(event.pos):
                    self.input_box_active = True
                else:
                    self.input_box_active = False
                if self.scrollbar_rect and self.scrollbar_rect.collidepoint(event.pos):
                    self.dragging_scrollbar = True
                    self.scrollbar_start_y = event.pos[1]

    def handle_mouse_release(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            self.dragging_scrollbar = False

    def handle_mouse_scroll(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.menu_open and event.button == 4:  # Rueda hacia arriba
                self.scroll_offset = max(0, self.scroll_offset - self.scroll_speed)
            elif self.menu_open and event.button == 5:  # Rueda hacia abajo
                total_list_height = len(self.filtered_blocks) * (self.font.get_height() + 2)
                max_scroll_offset = max(0, total_list_height - (self.menu_rect.height - self.input_box.height - 40))
                self.scroll_offset = min(max_scroll_offset, self.scroll_offset + self.scroll_speed)

    def handle_keypress(self, event):
        if event.type == pygame.KEYDOWN and self.input_box_active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key == pygame.K_RETURN:
                self.filtered_blocks = [block for block in BLOCK_LIST if self.text.lower() in block.lower()]
            else:
                self.text += event.unicode
