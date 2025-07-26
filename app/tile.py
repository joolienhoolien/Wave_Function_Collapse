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
import configparser
from typing import Self


#Constants should be imported by a settings.py file or config file of some sort
class Tile:
    def __init__(self, image_path: str, sides, rotations=0, full_image_path=False):
        #Sides describes the tags of the side. i.e. building a map it could be "wood", "tree", "unwalkable"
        config = configparser.ConfigParser()
        config.read('../settings.ini')
        self.up = int(config['tiles']['UP'])
        self.right = int(config['tiles']['RIGHT'])
        self.left = int(config['tiles']['LEFT'])
        self.down = int(config['tiles']['DOWN'])
        self.sides = sides
        self.valid_neighbors = {self.up: set(),
                                self.down: set(),
                                self.left: set(),
                                self.right: set()}
        if not full_image_path:
            base_path = f"../{config['tiles']['TILE_SET_FOLDER']}"
            tile_set_name = config["tiles"]["TILE_SET_NAME"]
            tile_set_filepath = f"{base_path}/{tile_set_name}"
            self.image_path = f"{tile_set_filepath}/{image_path}"
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
            if other_tile.sides[self.down] == self.sides[self.up][::-1]:
                self.valid_neighbors[self.up].add(other_tile)
            #UP
            if other_tile.sides[self.up] == self.sides[self.down][::-1]:
                self.valid_neighbors[self.down].add(other_tile)
            #RIGHT
            if other_tile.sides[self.left] == self.sides[self.right][::-1]:
                self.valid_neighbors[self.right].add(other_tile)
            #LEFT
            if other_tile.sides[self.right] == self.sides[self.left][::-1]:
                self.valid_neighbors[self.left].add(other_tile)

    def copy_tile_and_rotate(self, rotations: int) -> Self:
        sides = copy.deepcopy(self.sides)
        if rotations == 1:
            sides[self.up] = self.sides[self.left]
            sides[self.right] = self.sides[self.up]
            sides[self.down] = self.sides[self.right]
            sides[self.left] = self.sides[self.down]
        elif rotations == 2:
            sides[self.up] = self.sides[self.down]
            sides[self.right] = self.sides[self.left]
            sides[self.down] = self.sides[self.up]
            sides[self.left] = self.sides[self.right]
        elif rotations == 3:
            sides[self.up] = self.sides[self.right]
            sides[self.right] = self.sides[self.down]
            sides[self.down] = self.sides[self.left]
            sides[self.left] = self.sides[self.up]
        return Tile(sides=sides, image_path=self.image_path, rotations=rotations, full_image_path=True)