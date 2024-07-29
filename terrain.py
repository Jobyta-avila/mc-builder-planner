import numpy as np

class Terrain:
    def __init__(self, width, height):
        self.grid = np.zeros((width, height), dtype=int)
    
    def place_block(self, x, y, block_type):
        self.grid[x, y] = block_type
    
    def remove_block(self, x, y):
        self.grid[x, y] = 0
    
    def generate_material_list(self):
        unique, counts = np.unique(self.grid, return_counts=True)
        return dict(zip(unique, counts))
