import pygame

# Define los colores
GRID_COLOR = (0, 0, 0)  # Negro

class Grid2D:
    def __init__(self, screen, block_size=20):
        self.screen = screen
        self.block_size = block_size
        self.zoom_step = 1
        self.min_block_size = 10
        self.max_block_size = 100
        self.offset_x = 0
        self.offset_y = 0
        self.dragging = False
        self.last_mouse_x = 0
        self.last_mouse_y = 0

    def update_screen_size(self, screen):
        self.screen = screen

    def draw_grid(self):
        width, height = self.screen.get_size()
        
        # Dibuja las líneas verticales
        for x in range(self.offset_x % self.block_size, width, self.block_size):
            pygame.draw.line(self.screen, (200, 200, 200), (x, 0), (x, height))
        
        # Dibuja las líneas horizontales
        for y in range(self.offset_y % self.block_size, height, self.block_size):
            pygame.draw.line(self.screen, (200, 200, 200), (0, y), (width, y))

    def handle_zoom(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == pygame.BUTTON_WHEELUP:
                self.block_size += self.zoom_step
                if self.block_size > self.max_block_size:
                    self.block_size = self.max_block_size
            elif event.button == pygame.BUTTON_WHEELDOWN:
                self.block_size -= self.zoom_step
                if self.block_size < self.min_block_size:
                    self.block_size = self.min_block_size

    def handle_drag(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Botón izquierdo del ratón
                self.dragging = True
                self.last_mouse_x, self.last_mouse_y = event.pos
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Botón izquierdo del ratón
                self.dragging = False
        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                dx = event.pos[0] - self.last_mouse_x
                dy = event.pos[1] - self.last_mouse_y
                self.offset_x += dx
                self.offset_y += dy
                self.last_mouse_x, self.last_mouse_y = event.pos


    def update(self, event):
        self.handle_zoom(event)
        self.handle_drag(event)
