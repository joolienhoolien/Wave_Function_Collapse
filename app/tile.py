"""
Tile class responsibilities:
    - Define a set of rules for a tile
        - Holds an image path pointing to disk
        - Holds info on side types (i.e. UP = connection, DOWN = blank)
        - Holds info on which other tiles are valid neighbors
            This is set up after every tile is created.
    - Used as a blueprint when collapsing cells
"""

BLANK, UP, RIGHT, DOWN, LEFT = 0, 1, 2, 3, 4

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
            if other_tile.sides[DOWN] & self.sides[UP]:
                self.neighbors[DOWN].add(other_tile)
            #UP
            if other_tile.sides[UP] & self.sides[DOWN]:
                self.neighbors[UP].add(other_tile)
            #RIGHT
            if other_tile.sides[LEFT] & self.sides[RIGHT]:
                self.neighbors[LEFT].add(other_tile)
            #LEFT
            if other_tile.sides[RIGHT] & self.sides[LEFT]:
                self.neighbors[RIGHT].add(other_tile)

"""
In the setup() phase of the program
we need to take in a set of base tiles
alter them (rotate, flip, i think that's it)
store list of all tiles in main.py.

Then, once we have the list, we need to go through it
for each tile, we look for other tiles which match 
add the acceptable tiles to neighbors set
i.e.
tile_apple.sides.UP = set(1, 4)
look through tiles
    tile.banana.down = 0 -> don't add it to tile_apples neighbors
    tile.orange.down = 1 -> add it!
        tile.apple.neighbors[UP] += tile.orange

Then we set up our cells...

Then when we collapse...
we pick a cell and collapse it,
look at the neighbors and do the same check as before
cell.options = cell.options & currentTile.neighbors[{direction}]


Optimization:
Have a separate data structure for keeping track of least entropic 
cells and removes collapsed cells so that performance keeps up
"""