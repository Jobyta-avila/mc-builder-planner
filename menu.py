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
    'Ancient Debris', 'Andesite', 'Anvil', 'Azalea',
    'Bamboo', 'Bamboo Mosaic', 'Banner', 'Barrel', 'Barrier', 'Basalt',
    'Beacon', 'Bed', 'Bedrock', 'Beehive', 'Beetroot Seeds', 'Bell',
    'Big Dripleaf', 'Big Sign', 'Blackstone', 'Blast Furnace', 'Block of Amethyst',
    'Block of Bamboo', 'Block of Coal', 'Block of Copper', 'Block of Diamond',
    'Block of Emerald', 'Block of Gold', 'Block of Iron', 'Block of Lapis Lazuli',
    'Block of Netherite', 'Block of Quartz', 'Block of Raw Copper',
    'Block of Raw Gold', 'Block of Raw Iron', 'Block of Redstone', 'Blue Ice',
    'Bone Block', 'Bookshelf', 'Border', 'Box of Infinite Books', 'Brewing Stand',
    'Bricks', 'Bubble Column', 'Budding Amethyst', 'Button', 'Cactus', 'Cake',
    'Calcite', 'Calibrated Sculk Sensor', 'Campfire', 'Candle', 'Carpet',
    'Carrot', 'Cartography Table', 'Cauldron', 'Chain', 'Chalkboard', 'Cheese',
    'Chest', 'Chiseled Bookshelf', 'Chiseled Deepslate', 'Chorus Flower',
    'Chorus Plant (block)', 'Clay', 'Clay Pot', 'Client request placeholder block',
    'Coal Ore', 'Coarse Dirt', 'Cobbled Deepslate', 'Cobblestone', 'Cobweb',
    'Cocoa Beans', 'Colored Torch', 'Command Block', 'Composter',
    'Compound Creator', 'Concrete', 'Concrete Powder', 'Conduit', 'Copper Ore',
    'Copper Sink', 'Copper Spleaves', 'Coral', 'Coral Block', 'Coral Fan',
    'Crafting Table', 'Crying Obsidian', 'Cursor', 'Daylight Detector', 'Dead Bush',
    'Decorated Pot', 'Deepslate', 'Deepslate Bricks', 'Deepslate Tiles',
    'Detector Rail', 'Diamond Ore', 'Diorite', 'Dirt', 'Dirt Path', 'Dispenser',
    'Door', 'Dragon Egg', 'Dried Kelp Block', 'Dripstone Block', 'Dropper',
    'Element', 'Element Constructor', 'Emerald Ore', 'Enchanting Table',
    'End Gateway (block)', 'End Portal (block)', 'End Portal Frame', 'End Rod',
    'End Stone', 'End Stone Bricks', 'Ender Chest', 'Etho Slab', 'Farmland',
    'Fence', 'Fence Gate', 'Fire', 'Fletching Table', 'Flower', 'Flower Pot',
    'Fluid', 'Foundation block', 'Froglight', 'Frogspawn', 'Frosted Ice',
    'Fungus', 'Funky Portal', 'Furnace', 'Gear', 'Gilded Blackstone', 'Glass',
    'Glass Pane', 'Glazed Terracotta', 'Glow Berries', 'Glow Lichen',
    'Glowing Obsidian', 'Glowstone', 'Gold Ore', 'Golden Chest', 'Granite',
    'Grass', 'Grass Block', 'Grass carried', 'Gravel', 'Green Shrub', 'Grindstone',
    'Hanging Roots', 'Hardened Glass', 'Hardened Glass Pane', 'Hay Bale', 'Head',
    'Heat Block', 'Home Block', 'Honey Block', 'Honeycomb Block', 'Hopper',
    'How did we get here? (block)', 'Ice', 'Infested Block', 'Info update',
    'Information block', 'Information Sign', 'Invisible Bedrock', 'Iron Bars',
    'Iron Ore', 'Item Frame', 'Jack o\'Lantern', 'Jigsaw Block', 'Jukebox',
    'Kelp', 'Lab Table', 'Ladder', 'Lantern', 'Lapis Lazuli Ore', 'Lava',
    'Lava Spawner', 'Leaves', 'Leaves carried', 'Lectern', 'Leftover', 'Lever',
    'Light', 'Light Block', 'Lightning Rod', 'Lily Pad', 'Locked chest', 'Lodestone',
    'Log', 'Loom'
]

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.menu_width = 300
        self.menu_open = False
        self.font = pygame.font.SysFont(None, 18)
        self.input_font = pygame.freetype.SysFont(None, 20)
        self.update_menu_rect()  # Llama a este método después de inicializar los atributos relevantes
        self.back_button_rect = None
        self.scroll_offset = 0
        self.scroll_speed = 10
        self.input_box = pygame.Rect(10, 10, self.menu_width - 20, 30)
        self.text = ''
        self.filtered_blocks = BLOCK_LIST
        self.dragging_scrollbar = False
        self.scrollbar_start_y = 0

    def update_menu_rect(self):
        self.menu_rect = pygame.Rect(0, 0, self.menu_width, self.screen.get_height())
        self.input_box = pygame.Rect(10, 10, self.menu_width - 20, 30)
        self.max_visible_blocks = self.calculate_max_visible_blocks()

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
        y_offset = self.input_box.bottom + 10 - self.scroll_offset
        start_index = int(self.scroll_offset // (self.font.get_height() + 2))
        end_index = int(start_index + self.max_visible_blocks)
        blocks_to_draw = self.filtered_blocks[start_index:end_index]
    
        for block in blocks_to_draw:
            text = self.font.render(block, True, TEXT_COLOR)
            if y_offset > self.menu_rect.height - 30:  # Ajusta el límite para evitar superposición
                break
            self.screen.blit(text, (10, y_offset))
            y_offset += self.font.get_height() + 2
        
        # Ajusta el desplazamiento máximo para asegurarse de que se muestre el último bloque
        total_list_height = len(self.filtered_blocks) * (self.font.get_height() + 2)
        if total_list_height > self.menu_rect.height - self.input_box.height:
            self.scroll_offset = min(
                self.scroll_offset,
                total_list_height - (self.menu_rect.height - self.input_box.height)
            )

    def draw_back_button(self):
        back_text = self.font.render('Back', True, TEXT_COLOR)
        self.back_button_rect = pygame.Rect(10, self.screen.get_height() - 40, self.menu_width - 20, 30)
        pygame.draw.rect(self.screen, (150, 150, 150), self.back_button_rect)
        self.screen.blit(back_text, (self.back_button_rect.x + 5, self.back_button_rect.y + (self.back_button_rect.height - back_text.get_height()) // 2))

    def draw_scroll_bar(self):
        if len(self.filtered_blocks) * (self.font.get_height() + 2) > self.menu_rect.height:
            scrollbar_height = max(30, self.menu_rect.height * (self.menu_rect.height / (len(self.filtered_blocks) * (self.font.get_height() + 2))))
            scrollbar_y = self.scroll_offset * (self.menu_rect.height - scrollbar_height) / (len(self.filtered_blocks) * (self.font.get_height() + 2) - self.menu_rect.height)
            scrollbar_rect = pygame.Rect(self.menu_rect.width - 10, scrollbar_y, 10, scrollbar_height)
            pygame.draw.rect(self.screen, SCROLL_BAR_COLOR, scrollbar_rect)
            return scrollbar_rect
        return None

    def handle_mouse_motion(self, event):
        if event.type == pygame.MOUSEMOTION:
            if self.menu_rect.collidepoint(event.pos):
                self.menu_open = True
            if self.dragging_scrollbar:
                scrollbar_rect = self.draw_scroll_bar()
                if scrollbar_rect:
                    scrollbar_y = event.pos[1] - self.scrollbar_start_y
                    self.scroll_offset = min(
                        max(0, self.scroll_offset + scrollbar_y * (len(self.filtered_blocks) * (self.font.get_height() + 2) - self.menu_rect.height) / (self.menu_rect.height - scrollbar_rect.height)),
                        len(self.filtered_blocks) * (self.font.get_height() + 2) - self.menu_rect.height
                    )
                    self.scrollbar_start_y = event.pos[1]

    def handle_mouse_click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.menu_rect.collidepoint(event.pos):
                if self.draw_scroll_bar() and self.draw_scroll_bar().collidepoint(event.pos):
                    self.dragging_scrollbar = True
                    self.scrollbar_start_y = event.pos[1] - self.draw_scroll_bar().y
                elif self.back_button_rect and self.back_button_rect.collidepoint(event.pos):
                    self.menu_open = False
            else:
                self.menu_open = False

    def handle_mouse_release(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            if self.dragging_scrollbar:
                self.dragging_scrollbar = False

    def handle_mouse_scroll(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 4:  # Rueda hacia arriba
            self.scroll_offset = max(0, self.scroll_offset - self.scroll_speed)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 5:  # Rueda hacia abajo
            self.scroll_offset = min(
                len(self.filtered_blocks) * (self.font.get_height() + 2) - (self.menu_rect.height - self.input_box.height),
                self.scroll_offset + self.scroll_speed
            )

    def handle_keypress(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key == pygame.K_RETURN:
                # Aquí puedes agregar la lógica para la acción del enter
                pass
            else:
                self.text += event.unicode
            self.filtered_blocks = [block for block in BLOCK_LIST if self.text.lower() in block.lower()]
            self.scroll_offset = 0  # Resetea el desplazamiento al filtrar
            self.max_visible_blocks = self.calculate_max_visible_blocks()
