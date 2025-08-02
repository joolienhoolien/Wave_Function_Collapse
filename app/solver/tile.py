import copy
import configparser
from typing import Self


class Tile:
    """
    Prototype class for defining a set of rules for a tile. Think of it like a blueprint for a node.
    A node will have a list of tiles which represents the different superpositions of tiles it can be.
    """
    def __init__(self, image_path: str, sides, rotations=0, full_image_path=False, config=None, weight=1):
        """
        - Define a set of rules for a tile
            - Holds an image path pointing to disk
            - Holds info on side types (i.e. UP = connection, DOWN = blank)
            - Holds info on which other tiles are valid neighbors
                This is set up after every tile is created.
            - Holds info on how many rotations
                - Useful for whatever class is rendering the images.
        - Used as a blueprint when collapsing cells
        :param sides: definition for the side. Tiles are valid next to each other when their sides match.
        :param rotations: How many permutations of this tile by rotation are there?
        :param image_path: The file name of the image or full path, depending on full_image_path parameter.
        :param full_image_path: Boolean detailing if image_path is a full path or just the filename
        :param config: configParser used to read settings.ini for initialization
        """
        if config is None:
            config = configparser.ConfigParser()
            config.read('../../settings.ini')
        self.config = config
        if not full_image_path:
            self.image_path = (f"../../{config['tiles']['TILE_SET_FOLDER']}/"
                               f"{config["tiles"]["TILE_SET_NAME"]}/{image_path}")
        else:
            self.image_path = f"{image_path}"
        self.id = ext_id
        self.sides = sides
        self.rotations = rotations
        self.weight = weight

        #Directions
        self.valid_neighbors = {direction:set() for direction in sides}
        self.directions = (config['tiles']['DIRECTIONS']).split(',')


    def __str__(self):
        """Lists the sides definition"""
        return f"Tile({self.id}_{self.rotations}_{self.sides})"


    def set_valid_neighbors(self, tiles) -> None:
        """
        Given a set of tiles, sets up a list of valid neighbors for this tile by comparing their sides.
        Parameter:
            tiles: a set of tiles
        """
        up, right, down, left = self.directions
        for other_tile in tiles:
            #DOWN
            if other_tile.sides[down] == self.sides[up][::-1]:
                self.valid_neighbors[up].add(other_tile)
            #UP
            if other_tile.sides[up] == self.sides[down][::-1]:
                self.valid_neighbors[down].add(other_tile)
            #RIGHT
            if other_tile.sides[left] == self.sides[right][::-1]:
                self.valid_neighbors[right].add(other_tile)
            #LEFT
            if other_tile.sides[right] == self.sides[left][::-1]:
                self.valid_neighbors[left].add(other_tile)

    def copy_tile_and_rotate(self, rotations: int) -> Self:
        """
        Given a number of times to rotate, rotates the tile.
        :param rotations: Number of times to rotate
        :return:
            New tile instance after rotation
        """
        sides = copy.deepcopy(self.sides)
        up, right, down, left = self.directions
        if rotations == 1:
            sides[up] = self.sides[left]
            sides[right] = self.sides[up]
            sides[down] = self.sides[right]
            sides[left] = self.sides[down]
        elif rotations == 2:
            sides[up] = self.sides[down]
            sides[right] = self.sides[left]
            sides[down] = self.sides[up]
            sides[left] = self.sides[right]
        elif rotations == 3:
            sides[up] = self.sides[right]
            sides[right] = self.sides[down]
            sides[down] = self.sides[left]
            sides[left] = self.sides[up]
        return Tile(ext_id=self.id, sides=sides, image_path=self.image_path,
                    rotations=rotations, full_image_path=True,
                    config=self.config, weight=self.weight)