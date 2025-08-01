import random
from app.solver.tile import Tile
from app.solver.node import Node
import json


class Grid:
    """
    A collection of data used for solving a wave function collapse problem.
    """
    def __init__(self, tile_set_filepath, width, height, directions, debug=False):
        """
        Instance of a grid used for wave function collapse
            finished_collapsing: Whether the grid has been collapsed or not
            grid: the 2d grid of nodes representing the wave
            width, height: dimensions of the 2d grid
            all_tiles: set of all tiles after permutations
        """
        self.finished_collapsing = False
        self.base_tiles = import_tileset(tile_set_filepath)
        self.all_tiles = permute_tiles(self.base_tiles)
        self.width = width
        self.height = height
        self.grid = self.set_new_grid()
        self.debug = debug
        self.directions = directions
        self.failed_collapsing = False

    #Get/set
    def is_finished_collapsing(self):
        """Returns whether the grid is finished collapsing"""
        return self.finished_collapsing

    def get_lowest_entropy_nodes(self):
        """Helper function that returns a list of nodes with the lowest entropy."""
        lowest_entropy = len(self.all_tiles)
        lowest_entropy_nodes = []
        for row in self.grid:
            for node in row:
                if (node.is_collapsed() or
                        (options := len(node.get_tile_options())) > lowest_entropy):
                    continue
                elif options == lowest_entropy:
                    lowest_entropy_nodes.append(node)
                else:
                    lowest_entropy = options
                    lowest_entropy_nodes = [node]
        return lowest_entropy_nodes

    def propagate(self, node: Node):
        """When a node is collapsed, this function is called. Propagates the collapse to neighboring nodes.
        Parameters:
            node: the collapsed node

        Returns:
            True if the propagation was successful, False otherwise."""
        try:
            # Propagate
            stack = [node]
            while stack:
                curr_node = stack.pop()
                for direction in self.directions:
                    other_node = None
                    if direction == "left":
                        other_node = self.grid[(curr_node.x - 1) % self.width][curr_node.y]
                    elif direction == "right":
                        other_node = self.grid[(curr_node.x + 1) % self.width][curr_node.y]
                    elif direction == "up":
                        other_node = self.grid[curr_node.x][(curr_node.y - 1) % self.height]
                    elif direction == "down":
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
            return True
        except AttributeError:
            print(f"found contradiction in cell ({node.x},{node.y})")
            self.finished_collapsing = True
            return False

    def collapse_node(self, coordinates=None, tile_options=None):
        """Collapse the next tile on the grid.
        Returns:
            True if we are out of nodes to collapse or the node was collapsed successfully.
            False if there was an issue collapsing."""
        if coordinates is None or tile_options is None:
            # 1. Obtain a list of tiles coordinates such that they have the least amount of options
            lowest_entropy_nodes = self.get_lowest_entropy_nodes()
            if not lowest_entropy_nodes:
                self.finished_collapsing = True
                return True

            # 2. From this list, randomly choose a tile to collapse
            node = random.choice(lowest_entropy_nodes)
        else:
            node = self.grid[coordinates[0]][coordinates[1]]
        if tile_options:
            tile_options = {tile_options}
        if not node.collapse(tile_options=tile_options):
            print(f"found contradiction in node ({node.x},{node.y})")
            self.finished_collapsing = True
            self.failed_collapsing = True
            return node

        return node if self.propagate(node) else None

    def set_new_grid(self):
        """Initialized the grid.
        Parameters:
            all_tiles: set of all tiles after permutations
            width: width of the grid
            height: height of the grid"""
        # Set up neighbors for tiles
        for tile in self.all_tiles:
            tile.set_valid_neighbors(self.all_tiles)

        # Set up grid of nodes
        grid = [[Node(i, j, self.all_tiles) for j in range(self.height)] for i in range(self.width)]
        return grid

    def reset(self):
        self.finished_collapsing = False
        self.failed_collapsing = False
        self.grid = self.set_new_grid()
        return True


def import_tileset(filepath):
    """Given a filepath to the tileset, creates a set of base tiles.
    Parameters:
        filepath: the filepath to the tileset
    Returns:
        Set of base tiles."""
    try:
        base_tiles = []
        with open(filepath, 'r') as file:
            data = json.load(file)
        for tile in data['tile_set']:
            sides = {side.lower(): value for i, (side, value) in enumerate(tile['sides'].items())}
            try:
                weight = tile['weight']
            except KeyError as error:
                weight = 1
            base_tiles.append(Tile(image_path=tile['image_path'],
                                   sides=sides,
                                   rotations=tile['number_of_rotations'],
                                   weight=weight))
        return base_tiles
    except FileNotFoundError as error:
        print(error)
        raise


def permute_tiles(base_tiles):
    """Given a set of basic tiles, permutes them base on the instructions on the tile itself.
    Parameters:
        base_tiles: List of base tiles to be permuted
    Returns:
        list of permuted tiles"""
    permuted_tiles = []
    for tile in base_tiles:
        if tile.rotations == 0:
            permuted_tiles.append(tile)
        else:
            for rotation in range(tile.rotations):
                permuted_tiles.append(tile.copy_tile_and_rotate(rotation))
    return permuted_tiles







