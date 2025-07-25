"""
Tile class responsibilities:
    - Define a set of rules for a tile
        - Holds an image path pointing to disk
        - Holds info on side types (i.e. UP = connection, DOWN = blank)
        - Holds info on which other tiles are valid neighbors
            This is set up after every tile is created.
        - Holds info on how many rotations
            - Useful for whatever class is rendering the images.
    - Used as a blueprint when collapsing cells
"""
import copy
from PIL import Image
from settings import UP, RIGHT, DOWN, LEFT, TILE_SET_FILEPATH_BASE

#Constants should be imported by a settings.py file or config file of some sort
class Tile:
    def __init__(self, image_path: str, sides, rotations=0, full_image_path=False):
        #Sides describes the tags of the side. i.e. building a map it could be "wood", "tree", "unwalkable"
        self.sides = sides
        self.valid_neighbors = {UP: set(),
                                DOWN: set(),
                                LEFT: set(),
                                RIGHT: set()}
        if not full_image_path:
            self.image_path = f"{TILE_SET_FILEPATH_BASE}{image_path}"
        else:
            self.image_path = f"{image_path}"
        self.rotations = rotations
        #if image_path: self.image = Image.open(image_path)
        #elif image: self.image = image

    def __str__(self):
        return f"{self.sides}"
    #TODO: Can be optimized to O(nlogn) instead of O(n^2)
    #Currently this will be called by a for loop so it checks each tile against each other tile,
    #   redundantly checking both directions for each tile twice
    #   i.e. check tile 0 against tile 1 on first loop, then checks 1 against 0 on second loop
    #   Could maybe just have a check for "if this tile is in my neighbors already, skip"?
    #   Use two pointers to iterate through
    def set_valid_neighbors(self, tiles) -> None:
        for other_tile in tiles:
            #DOWN
            if other_tile.sides[DOWN] == self.sides[UP][::-1]:
                self.valid_neighbors[UP].add(other_tile)
            #UP
            if other_tile.sides[UP] == self.sides[DOWN][::-1]:
                self.valid_neighbors[DOWN].add(other_tile)
            #RIGHT
            if other_tile.sides[LEFT] == self.sides[RIGHT][::-1]:
                self.valid_neighbors[RIGHT].add(other_tile)
            #LEFT
            if other_tile.sides[RIGHT] == self.sides[LEFT][::-1]:
                self.valid_neighbors[LEFT].add(other_tile)

def copy_tile_and_rotate(tile: Tile, rotations: int) -> Tile:
    sides = copy.deepcopy(tile.sides)
    if rotations == 1:
        sides[UP] = tile.sides[LEFT]
        sides[RIGHT] = tile.sides[UP]
        sides[DOWN] = tile.sides[RIGHT]
        sides[LEFT] = tile.sides[DOWN]
    elif rotations == 2:
        sides[UP] = tile.sides[DOWN]
        sides[RIGHT] = tile.sides[LEFT]
        sides[DOWN] = tile.sides[UP]
        sides[LEFT] = tile.sides[RIGHT]
    elif rotations == 3:
        sides[UP] = tile.sides[RIGHT]
        sides[RIGHT] = tile.sides[DOWN]
        sides[DOWN] = tile.sides[LEFT]
        sides[LEFT] = tile.sides[UP]
    return Tile(sides=sides, image_path=tile.image_path, rotations=rotations, full_image_path=True)