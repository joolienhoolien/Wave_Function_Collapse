import random

from app.solver.tile import Tile
from app.solver.node import Node
import json


class Grid:
    def __init__(self, tile_set_filepath, width, height, debug=False):
        self.finished_collapsing = False
        self.base_tiles = import_tileset(tile_set_filepath)
        self.all_tiles = permute_tiles(self.base_tiles)
        self.grid = set_new_grid(self.all_tiles, width, height)
        self.width = width
        self.height = height
        self.debug=debug

    #Get/set
    def is_finished_collapsing(self):
        return self.finished_collapsing

    def collapse_next_tile(self):
        # 1. Obtain a list of tiles coordinates such that they have the least amount of options
        lowest_entropy = len(self.all_tiles)
        lowest_entropy_nodes = []
        for row in self.grid:
            for node in row:
                if node.is_collapsed() or len(node.get_tile_options()) > lowest_entropy:
                    continue
                elif len(node.get_tile_options()) == lowest_entropy:
                    lowest_entropy_nodes.append(node)
                else:
                    lowest_entropy = len(node.get_tile_options())
                    lowest_entropy_nodes = [node]

        # 2. From this list, randomly choose a tile to collapse
        if lowest_entropy_nodes:
            to_collapse_data = random.choice(lowest_entropy_nodes)
            node = to_collapse_data
            if self.debug: print(f"Collapsing {to_collapse_data}")
            if not node.collapse():
                print(f"found contradiction in node ({node.x},{node.y})")
                self.finished_collapsing = True
                return False, node.x, node.y

            # 3. Propagate
            try:
                UP, RIGHT, DOWN, LEFT = 1, 2, 3, 4

                #Propagate
                stack = [node]
                while stack:
                    curr_node = stack.pop()
                    for direction in [UP, RIGHT, DOWN, LEFT]:
                        other_node = None
                        if direction == LEFT:
                            other_node = self.grid[(curr_node.x - 1) % self.width][curr_node.y]
                        elif direction == RIGHT:
                            other_node = self.grid[(curr_node.x + 1) % self.width][curr_node.y]
                        elif direction == UP:
                            other_node = self.grid[curr_node.x][(curr_node.y - 1) % self.height]
                        elif direction == DOWN:
                            other_node = self.grid[curr_node.x][(curr_node.y + 1) % self.height]
                        other_tiles = other_node.get_tile_options()
                        possible_neighbors = curr_node.get_valid_neighbors(direction)
                        if len(possible_neighbors) == 0: continue

                        for other_tile in other_tiles:
                            if not other_tile in possible_neighbors:
                                other_tile_options = set()
                                other_tile_options.add(other_tile)
                                new_options = other_tiles - other_tile_options
                                other_node.set_tile_options(tile_options=new_options & other_node.get_tile_options())
                                if not other_node in stack:
                                    stack.append(other_node)
            except AttributeError:
                    print(f"found contradiction in cell ({node.x},{node.y})")
                    self.finished_collapsing = True
                    return False, node.x, node.y
        #2.b: we are out of nodes to collapse.
        else:
            self.finished_collapsing = True
        return True, None, None


def import_tileset(filepath):
    try:
        base_tiles = []
        with open(filepath, 'r') as file:
            data = json.load(file)
        for tile in data['tile_set']:
            sides = {i + 1: value for i, (side, value) in enumerate(tile['sides'].items())}
            base_tiles.append(Tile(image_path=tile['image_path'], sides=sides,
                                                                rotations=tile['number_of_rotations']))
        return base_tiles
    except FileNotFoundError as error:
        print(error)
        raise


def permute_tiles(base_tiles):
    permuted_tiles = []
    for tile in base_tiles:
        if tile.rotations == 0:
            permuted_tiles.append(tile)
        else:
            for rotation in range(tile.rotations):
                permuted_tiles.append(tile.copy_tile_and_rotate(rotation))
    return permuted_tiles


def set_new_grid(all_tiles, width, height):
    # Set up neighbors for tiles
    for tile in all_tiles:
        tile.set_valid_neighbors(all_tiles)

    # Set up grid of nodes
    grid = [[Node(i, j, all_tiles) for j in range(height)] for i in range(width)]
    return grid






