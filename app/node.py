"""
Responsible for:
    data:
    - x, y coordinates in it's parent grid
    - set of current options for which tile it can be
    - collapsed state
    - if collapsed, it's tile
    - image or image path
    func:
    - Collapsing itself into a tile
        - If given a tile to collapse into, picks that one
        - Else, randomly choose from current options
        - updating image or image path
"""
import random


class Node:
    def __init__(self, x, y, tile_options):
        self.x = x
        self.y = y
        self.tile_options = set(tile_options)
        self.collapsed = False
        self.tile = None
        self.updated = False

    def __str__(self):
        return f'[{self.x}][{self.y}]: {self.tile}'

    def collapse(self):
        self.updated = True
        if not self.tile_options:
            return False
        else:
            self.set_tile(tile=random.choice(tuple(self.tile_options)))
            return True

    #Get/set
    def is_collapsed(self):
        return self.collapsed

    def get_tile_options(self):
        return self.tile_options

    def get_valid_neighbors(self, direction):
        result = []
        for tile in self.tile_options:
            result = result + list(tile.valid_neighbors[direction])
        return result

    def set_tile_options(self, tile_options):
        self.tile_options = tile_options
        self.updated = True

    def set_tile(self, tile):
        self.collapsed = True
        self.tile_options = set()
        self.tile_options.add(tile)
        self.tile = tile
        self.updated = True

    def set_updated(self, value=False):
        self.updated = value

    def get_updated(self):
        return self.updated

    def get_reset_updated(self):
        updated = self.updated
        self.updated = False
        return updated

    def get_collapsed(self):
        return self.collapsed