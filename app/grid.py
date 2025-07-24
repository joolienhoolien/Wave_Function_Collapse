import random

from tile import Tile, copy_tile_and_rotate
from node import Node
import json


class Grid:
    def __init__(self, tile_set_filepath, width, height):
        self.finished_collapsing = False
        self.base_tiles = import_tileset(tile_set_filepath)
        self.all_tiles = permute_tiles(self.base_tiles)
        self.grid = set_new_grid(self.all_tiles, width, height)
        self.width = width
        self.height = height

    #Get/set
    def is_finished_collapsing(self):
        return self.finished_collapsing

    def collapse_next_tile(self):
        # 1. Obtain a list of tiles coordinates such that they have the least amount of options
        lowest_entropy = len(self.all_tiles)
        lowest_entropy_nodes = []
        for i, row in enumerate(self.grid):
            for j, node in enumerate(row):
                if node.is_collapsed() or len(node.tile_options) > lowest_entropy:
                    continue
                elif len(node.tile_options) == lowest_entropy:
                    lowest_entropy_nodes.append((node, i, j))
                else:
                    lowest_entropy = len(node.tile_options)
                    lowest_entropy_nodes = [(node, i, j)]

        # 2. From this list, randomly choose a tile to collapse
        if lowest_entropy_nodes:
            to_collapse_data = random.choice(lowest_entropy_nodes)
            node, x, y = to_collapse_data
            if not node.collapse():
                print(f"found contradiction in node ({x},{y})")
                self.finished_collapsing = True
                return False, x, y

            # 3. Update neighboring tiles using intersection of rules and options
            try:
                UP, RIGHT, DOWN, LEFT = 1, 2, 3, 4

                stack = []

                #Add neighbors to stack if not collapsed
                node_left = self.grid[(x - 1) % self.width][y]
                if not node_left.is_collapsed():
                    stack.append(node_left)
                    #node_left.set_tile_options(node_left.tile_options & node.tile.valid_neighbors[RIGHT])
                node_right = self.grid[(x + 1) % self.width][y]
                if not node_right.is_collapsed():
                    stack.append(node_right)
                    #node_right.set_tile_options(node_right.options & node.tile.valid_neighbors[LEFT])
                node_up = self.grid[x][(y - 1) % self.height]
                if not node_up.is_collapsed():
                    stack.append(node_up)
                    #node_up.set_tile_options(node_up.options & node.tile.valid_neighbors[DOWN])
                node_down = self.grid[x][(y + 1) % self.height]
                if not node_down.is_collapsed():
                    stack.append(node_down)
                    #node_down.set_tile_options(node_down.options & node.tile.valid_neighbors[UP])

                #Propagate
                while stack:
                    curr_node = stack.pop()
                    if not curr_node.is_collapsed():
                        temp_options = curr_node.tile_options

                        # Calculate new options
                        #LEFT
                        tile_union = set()
                        node_left = self.grid[(x - 1) % self.width][y]
                        for tile in node_left.tile_options:
                            tile_union = tile_union | tile.valid_neighbors[RIGHT]
                        curr_node.tile_options = curr_node.tile_options & tile_union
                        # Check if updated
                        if not temp_options == curr_node.tile_options:
                            stack.append(node_left)

                        #RIGHT
                        tile_union = set()
                        node_right = self.grid[(x + 1) % self.width][y]
                        for tile in node_right.tile_options:
                            tile_union = tile_union | tile.valid_neighbors[LEFT]
                        curr_node.tile_options = curr_node.tile_options & tile_union
                        # Check if updated
                        if not temp_options == curr_node.tile_options:
                            stack.append(node_right)

                        #UP
                        tile_union = set()
                        node_up = self.grid[x][(y - 1) % self.height]
                        for tile in node_up.tile_options:
                            tile_union = tile_union | tile.valid_neighbors[DOWN]
                        curr_node.tile_options = curr_node.tile_options & tile_union
                        # Check if updated
                        if not temp_options == curr_node.tile_options:
                            stack.append(node_up)

                        #DOWN
                        tile_union = set()
                        node_down = self.grid[x][(y + 1) % self.height]
                        for tile in node_down.tile_options:
                            tile_union = tile_union | tile.valid_neighbors[UP]
                        curr_node.tile_options = curr_node.tile_options & tile_union

                        # Check if updated
                        if not temp_options == curr_node.tile_options:
                            stack.append(node_down)
            except AttributeError:
                    print(f"found contradiction in cell ({x},{y})")
                    self.finished_collapsing = True
                    return False, x, y
        #2.b: we are out of nodes to collapse.
        else:
            self.finished_collapsing = True
        return True, None, None


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
    grid = []#[[0 for _ in range(height)] for _ in range(width)]
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            grid[i][j] = Node(i, j, all_tiles)
    return grid






