import pygame
import logging

class Toolbar:
    def __init__(self, screen, height=60, margin_left=300, offset_y=40):
        self.screen = screen
        self.height = height
        self.offset_y = offset_y
        self.rect = pygame.Rect(margin_left, offset_y, screen.get_width() - margin_left, height)
        self.buttons = []
        self.selected_tool = None

    def add_button(self, image_path, tool_name):
        image = pygame.image.load(image_path)
        image = pygame.transform.scale(image, (40, 40))  # Escalar el icono a un tamaño razonable
        button_rect = image.get_rect()
        button_rect.y = self.offset_y + 5  # Margen desde la parte superior
        button_rect.x = self.rect.x + len(self.buttons) * (button_rect.width + 10)  # Espacio entre botones
        self.buttons.append({'rect': button_rect, 'image': image, 'tool_name': tool_name})

    def draw(self):
        pygame.draw.rect(self.screen, (180, 180, 180), self.rect)  # Fondo gris claro
        for button in self.buttons:
            self.screen.blit(button['image'], button['rect'])

    def handle_mouse_click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for button in self.buttons:
                if button['rect'].collidepoint(event.pos):
                    self.selected_tool = button['tool_name']
                    logging.debug(f"Herramienta seleccionada: {self.selected_tool}")
                    return self.selected_tool
        return None

    def update_screen_size(self, screen):
        self.screen = screen
        self.rect.width = screen.get_width() - self.rect.x  # Ajustar el ancho al tamaño de la pantalla actual
