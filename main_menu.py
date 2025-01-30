import pygame

class MainMenu:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 36)
        self.menu_items = ["File", "Settings", "Download", "Undo", "Redo"]
        self.menu_height = 40
        self.menu_rect = pygame.Rect(0, 0, screen.get_width(), self.menu_height)

    def draw(self):
        pygame.draw.rect(self.screen, (0, 0, 0), self.menu_rect)
        for i, item in enumerate(self.menu_items):
            text = self.font.render(item, True, (255, 255, 255))
            text_rect = text.get_rect(center=(self.screen.get_width() // len(self.menu_items) * (i + 0.5), self.menu_height // 2))
            self.screen.blit(text, text_rect)

    def update_screen_size(self, screen):
        self.screen = screen
        self.menu_rect.width = screen.get_width()

    def handle_mouse_click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for i, item in enumerate(self.menu_items):
                item_rect = pygame.Rect(self.screen.get_width() // len(self.menu_items) * i, 0, self.screen.get_width() // len(self.menu_items), self.menu_height)
                if item_rect.collidepoint(event.pos):
                    return item
        return None
