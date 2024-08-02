import pygame

class MainMenu:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 36)
        self.options = ["File", "Settings", "Download", "Undo", "Redo"]
        self.option_icons = [
            'assets/icons8-file-80.png',
            'assets/icons8-settings-80.png', 'assets/icons8-download-48.png',
            'assets/icons8-undo-48.png', 'assets/icons8-redo-48.png'
        ]
        self.menu_height = 40
        self.icons = self.load_icons()

    def load_icons(self):
        icons = []
        for icon_path in self.option_icons:
            icons.append(pygame.image.load(icon_path))
        return icons

    def draw(self):
        menu_rect = pygame.Rect(0, 0, self.screen.get_width(), self.menu_height)
        pygame.draw.rect(self.screen, (0, 0, 0), menu_rect)
        for i, option in enumerate(self.options):
            text = self.font.render(option, True, (255, 255, 255))
            text_rect = text.get_rect(center=(80 + i * 100, self.menu_height // 2))
            icon = pygame.transform.scale(self.icons[i], (20, 20))
            icon_rect = icon.get_rect(center=(60 + i * 100, self.menu_height // 2))
            self.screen.blit(icon, icon_rect)
            self.screen.blit(text, text_rect)

    def handle_mouse_click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for i, option in enumerate(self.options):
                text_rect = pygame.Rect(60 + i * 100 - 50, 0, 100, self.menu_height)
                if text_rect.collidepoint(event.pos):
                    return option
        return None

    def update_screen_size(self, screen):
        self.screen = screen
