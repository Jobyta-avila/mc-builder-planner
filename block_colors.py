import pygame

BLOCK_COLORS = {
    'Stone': (128, 128, 128),
    'Granite': (176, 114, 84),
    'Polished Granite': (189, 135, 109),
    'Diorite': (196, 196, 196),
    'Polished Diorite': (210, 210, 210),
    'Andesite': (136, 136, 136),
    'Polished Andesite': (149, 149, 149),
    'Deepslate': (50, 50, 50),
    'Cobbled Deepslate': (60, 60, 60),
    'Polished Deepslate': (70, 70, 70),
    'Calcite': (223, 224, 224),
    'Tuff': (79, 79, 79),
    'Dripstone Block': (143, 121, 79),
    'Grass Block': (89, 151, 71),
    'Dirt': (134, 96, 67),
    'Coarse Dirt': (126, 84, 46),
    'Podzol': (104, 72, 40),
    'Rooted Dirt': (149, 106, 60),
    'Mud': (64, 51, 34),
    'Crimson Nylium': (189, 68, 68),
    'Warped Nylium': (58, 118, 111),
    'Cobblestone': (131, 131, 131),
    'Sand': (219, 204, 158),
    'Red Sand': (191, 110, 64),
    'Gravel': (136, 126, 126),
    'Sandstone': (229, 221, 170),
    'Red Sandstone': (201, 116, 52),
    'Prismarine': (99, 194, 193),
    'Prismarine Bricks': (91, 185, 181),
    'Dark Prismarine': (47, 111, 113),
    'Netherrack': (110, 53, 49),
    'Basalt': (78, 78, 78),
    'Polished Basalt': (98, 98, 98),
    'Smooth Basalt': (69, 69, 69),
    'Soul Soil': (74, 57, 43),
    'End Stone': (221, 223, 158),
    'End Stone Bricks': (224, 226, 164),
    'Purpur Block': (169, 122, 169),
    'Purpur Pillar': (182, 138, 182),
    'Purpur Stairs': (182, 138, 182),
    'Purpur Slab': (182, 138, 182),
    'Oak Log': (114, 85, 57),
    'Spruce Log': (84, 64, 51),
    'Birch Log': (215, 204, 168),
    'Jungle Log': (155, 109, 77),
    'Acacia Log': (167, 91, 51),
    'Dark Oak Log': (60, 45, 29),
    'Mangrove Log': (90, 55, 55),
    'Bamboo Block': (194, 178, 128),
    'Crimson Stem': (122, 27, 27),
    'Warped Stem': (20, 122, 122),
    'Stripped Oak Log': (185, 140, 87),
    'Stripped Spruce Log': (141, 104, 74),
    'Stripped Birch Log': (218, 208, 170),
    'Stripped Jungle Log': (160, 118, 78),
    'Stripped Acacia Log': (192, 105, 66),
    'Stripped Dark Oak Log': (85, 58, 42),
    'Stripped Mangrove Log': (118, 63, 63),
    'Stripped Bamboo Block': (197, 180, 134),
    'Stripped Crimson Stem': (149, 38, 38),
    'Stripped Warped Stem': (26, 149, 149),
    'Oak Planks': (162, 130, 79),
    'Spruce Planks': (111, 81, 50),
    'Birch Planks': (200, 178, 127),
    'Jungle Planks': (167, 123, 85),
    'Acacia Planks': (180, 101, 59),
    'Dark Oak Planks': (71, 48, 32),
    'Mangrove Planks': (97, 56, 56),
    'Bamboo Planks': (183, 157, 85),
    'Crimson Planks': (134, 35, 35),
    'Warped Planks': (27, 134, 134)
    # Añade más bloques y sus colores aquí...
}

BLOCK_ICONS = {
    'Stone': 'assets/stone-block.png',
    # Añade otros bloques aquí con sus rutas de iconos
}

def load_block_icons():
    icons = {}
    for block, path in BLOCK_ICONS.items():
        try:
            icon = pygame.image.load(path).convert_alpha()
            icons[block] = icon
        except pygame.error as e:
            print(f"Error cargando el icono para {block}: {e}")
    return icons

