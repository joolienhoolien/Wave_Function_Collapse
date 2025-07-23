"""
Responsible for:
    - Settings (grid dimensions, fail condition, tile_set)
    - Creating and managing the grid
"""
from grid import Grid

class Solver:
    def __init__(self):
        #read settings from settings.json
        tile_set_filepath = ""
        self.grid = Grid(tile_set_filepath, width, height)