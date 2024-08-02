import pygame

class SaveMenu:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 36)
        self.menu_rect = pygame.Rect(0, 0, screen.get_width(), screen.get_height())
        self.options = ["Save as PDF", "Save as PNG", "Cancel"]
        self.selected_option = None

    def draw(self):
        self.screen.fill((255, 255, 255))
        for i, option in enumerate(self.options):
            text = self.font.render(option, True, (0, 0, 0))
            text_rect = text.get_rect(center=(self.screen.get_width() // 2, 150 + i * 50))
            self.screen.blit(text, text_rect)

    def handle_mouse_click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for i, option in enumerate(self.options):
                text_rect = pygame.Rect(self.screen.get_width() // 2 - 100, 150 + i * 50 - 20, 200, 40)
                if text_rect.collidepoint(event.pos):
                    self.selected_option = option
                    return option
        return None

    def update_screen_size(self, screen):
        self.screen = screen
        self.menu_rect.size = screen.get_size()
