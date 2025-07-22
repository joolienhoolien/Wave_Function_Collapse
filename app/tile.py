"""
Tile class responsibilities:
    - Define a set of rules for a tile
        - Holds an image path pointing to disk
        - Holds info on side types (i.e. UP = connection, DOWN = blank)
        - Holds info on which other tiles are valid neighbors
            This is set up after every tile is created.
    - Used as a blueprint when collapsing cells
"""
import copy

from PIL import Image
import os
from settings import UP, RIGHT, DOWN, LEFT

#Constants should be imported by a settings.py file or config file of some sort
class Tile:
    def __init__(self, image_path: str, sides):
        #Sides describes the tags of the side. i.e. building a map it could be "wood", "tree", "unwalkable"
        self.sides = sides
        self.image_path = image_path
        self.neighbors = {UP: set(),
                          DOWN: set(),
                          LEFT: set(),
                          RIGHT: set()}
    #TODO: Can be optimized to O(nlogn) instead of O(n^2)
    #Currently this will be called by a for loop so it checks each tile against each other tile,
    #   redundantly checking both directions for each tile twice
    #   i.e. check tile 0 against tile 1 on first loop, then checks 1 against 0 on second loop
    #   Could maybe just have a check for "if this tile is in my neighbors already, skip"?
    #   Use two pointers to iterate through
    def set_neighbors(self, tiles) -> None:
        for other_tile in tiles:
            #DOWN
            if other_tile.sides[DOWN] == self.sides[UP][::-1]:
                self.neighbors[DOWN].add(other_tile)
            #UP
            if other_tile.sides[UP] == self.sides[DOWN][::-1]:
                self.neighbors[UP].add(other_tile)
            #RIGHT
            if other_tile.sides[LEFT] == self.sides[RIGHT][::-1]:
                self.neighbors[LEFT].add(other_tile)
            #LEFT
            if other_tile.sides[RIGHT] == self.sides[LEFT][::-1]:
                self.neighbors[RIGHT].add(other_tile)

def rotate_tile(tile: Tile, num_pi_rotations: int) -> Tile:
    new_tile = Tile(tile.image_path, copy.deepcopy(tile.sides))

    #Rotate image to reflect the sides
    image = Image.open(new_tile.image_path)
    image = image.rotate(num_pi_rotations * -90)
    filepath, ext = os.path.splitext(tile.image_path)
    basename = os.path.basename(filepath)
    image_path = f"../tile_temp/{basename}{str(num_pi_rotations)}{ext}"
    image.save(image_path)
    new_tile.image_path = image_path

    #Rotate sides
    if num_pi_rotations == 1:
        new_tile.sides[UP] = tile.sides[LEFT]
        new_tile.sides[RIGHT] = tile.sides[UP]
        new_tile.sides[DOWN] = tile.sides[RIGHT]
        new_tile.sides[LEFT] = tile.sides[DOWN]
    elif num_pi_rotations == 2:
        new_tile.sides[UP] = tile.sides[DOWN]
        new_tile.sides[RIGHT] = tile.sides[LEFT]
        new_tile.sides[DOWN] = tile.sides[UP]
        new_tile.sides[LEFT] = tile.sides[RIGHT]
    elif num_pi_rotations == 3:
        new_tile.sides[UP] = tile.sides[RIGHT]
        new_tile.sides[RIGHT] = tile.sides[DOWN]
        new_tile.sides[DOWN] = tile.sides[LEFT]
        new_tile.sides[LEFT] = tile.sides[UP]
    return new_tile