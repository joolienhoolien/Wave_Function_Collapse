import random

class Node:
    """
    Representation of the data for a single node on the grid of the wave.
    """
    def __init__(self, x, y, tile_options):
        """
        Instantiates an instance of a node.
        x, y: coordinates on the grid
        tile_options: set of possibilities for which tile it can represent
        collapsed: current state of the node
        tile: if it is collapsed, the specific tile information for the node.
        updated: flag field for if the tile has been updated recently. Tells the GUI if it should reload the node's image
        """
        self.x = x
        self.y = y
        self.tile_options = set(tile_options)
        self.collapsed = False
        self.tile = None
        self.updated = False

    def __str__(self):
        """String representation of the node."""
        return f'[{self.x}][{self.y}]: {self.tile}'

    def collapse(self):
        """Collapse the node by randomly choosing from it's list of tile options.
        Returns:
            False if no options remain
            True if we set the tile and it was successful."""
        self.updated = True
        if not self.tile_options:
            return False
        tile_options_tuple = tuple(self.tile_options)
        tile_options_weights = [tile.weight for tile in tile_options_tuple]
        tile = random.choices(population=tile_options_tuple,
                              weights=tile_options_weights,
                              k=1)[0]
        return self.set_tile(tile=tile)

    def is_collapsed(self):
        """Returns if the tile is collapsed or not"""
        return self.collapsed

    def get_tile_options(self):
        """Returns the set of possibilities for which tile it can represent"""
        return self.tile_options

    def get_valid_neighbors(self, direction):
        """Returns the set of valid neighbors in a specific direction as a list (it is normally a set)"""
        result = []
        for tile in self.tile_options:
            result = result + list(tile.valid_neighbors[direction])
        return result

    def set_tile_options(self, tile_options):
        """Sets the set of possibilities for which tile can represent. Usually this is used during grid propagation."""
        self.tile_options = tile_options
        self.updated = True

    def set_tile(self, tile):
        """Attempts to set the node to a specific tile. Returns false if it does not work."""
        try:
            self.collapsed = True
            self.tile_options = set()
            self.tile_options.add(tile)
            self.tile = tile
            self.updated = True
            return True
        except AttributeError:
            return False

    def set_updated(self, value=False):
        """Sets flag field to signal GUI to refresh this node."""
        self.updated = value

    def get_updated(self):
        """Get flag field to signal GUI to refresh this node."""
        return self.updated

    def get_reset_updated(self):
        """Get flag field to signal GUI to refresh this node. Then, resets the flag field to false to
        signal we got the info."""
        updated = self.updated
        self.updated = False
        return updated

    def get_collapsed(self):
        """Get the node's collapsed state."""
        return self.collapsed