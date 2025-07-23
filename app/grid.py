from tile import Tile, copy_tile_and_rotate
from node import Node
import json


class Grid:
    def __init__(self, tile_set_filepath, width, height):
        self.finished_collapsing = False
        base_tiles = import_tileset(tile_set_filepath)
        all_tiles = permute_tiles(base_tiles)
        self.grid = set_new_grid(all_tiles, width, height)

    #Get/set
    def is_finished_collapsing(self):
        return self.finished_collapsing

def import_tileset(filepath):
    try:
        base_tiles = {
            4: [],
            2: [],
            0: []
        }
        with open(filepath, 'r') as file:
            data = json.load(file)
        for tile in data['tile_set']:
            sides = {i + 1: value for i, (side, value) in enumerate(tile['sides'].items())}
            base_tiles[tile['number_of_rotations']].append(Tile(tile['image_path'], sides))
        return base_tiles
    except FileNotFoundError as error:
        print(error)
        raise


def permute_tiles(base_tiles):
    permuted_tiles = []
    for num_rotations in base_tiles:
        for tile in base_tiles[num_rotations]:
            if num_rotations == 0:
                permuted_tiles.append(tile)
            else:
                for i in range(num_rotations):
                    permuted_tiles.append(copy_tile_and_rotate(tile, i))
    return permuted_tiles


def set_new_grid(all_tiles, width, height):
    # Set up neighbors for tiles
    for tile in all_tiles:
        tile.set_valid_neighbors(all_tiles)

    # Set up grid of nodes
    grid = [[0 for _ in range(height)] for _ in range(width)]
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            grid[i][j] = Node(i, j, all_tiles)
    return grid






