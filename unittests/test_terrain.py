import unittest
from terrain import Terrain

class TestTerrain(unittest.TestCase):

    def setUp(self):
        self.terrain = Terrain(10, 10)

    def test_place_block(self):
        self.terrain.place_block(1, 1, 2)
        self.assertEqual(self.terrain.grid[1, 1], 2)

    def test_remove_block(self):
        self.terrain.place_block(1, 1, 2)
        self.terrain.remove_block(1, 1)
        self.assertEqual(self.terrain.grid[1, 1], 0)

    def test_generate_material_list(self):
        self.terrain.place_block(1, 1, 2)
        self.terrain.place_block(1, 2, 3)
        self.terrain.place_block(1, 3, 2)
        material_list = self.terrain.generate_material_list()
        self.assertEqual(material_list, {0: 97, 2: 2, 3: 1})

if __name__ == '__main__':
    unittest.main()
