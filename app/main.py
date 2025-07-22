"""
In the setup() phase of the program
we need to take in a set of base tiles
alter them (rotate, flip, I think that's it)
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

import sys
from pygame.locals import *
import random
from tile import Tile, rotate_tile
from cell import Cell
from settings import *

FINISHED_COLLAPSING = False
TILES = []
grid = []

#Base tile's keys describe number of rotations to perform on the tile
BASE_TILES = {
    4: [],
    2: [],
    0: []
}

def setup_tiles_set1():
    BASE_TILES[0].append(Tile("../tile_sets/set1/blank.png",
                      {UP: "0", RIGHT: "0", DOWN: "0", LEFT: "0"}))
    BASE_TILES[4].append(Tile("../tile_sets/set1/T.png",
                           {UP: "1", RIGHT: "1", DOWN: "0", LEFT: "1"}))

def setup_tiles_pcb():
    """
    color definitions:
        GREY: 0
        GREEN: 1
        L GREEN: 2
        L GREY: 3
    :return:
    """
    BASE_TILES[0].append(Tile("../tile_sets/pcb/0.png",
                      {UP: "000", RIGHT: "000", DOWN: "000", LEFT: "000"}))
    BASE_TILES[0].append(Tile("../tile_sets/pcb/1.png",
                      {UP: "111", RIGHT: "111", DOWN: "111", LEFT: "111"}))
    BASE_TILES[4].append(Tile("../tile_sets/pcb/2.png",
                           {UP: "111", RIGHT: "121", DOWN: "111", LEFT: "111"}))
    BASE_TILES[2].append(Tile("../tile_sets/pcb/3.png",
                           {UP: "111", RIGHT: "131", DOWN: "111", LEFT: "131"}))
    BASE_TILES[4].append(Tile("../tile_sets/pcb/4.png",
                           {UP: "011", RIGHT: "121", DOWN: "110", LEFT: "000"}))
    BASE_TILES[4].append(Tile("../tile_sets/pcb/5.png",
                           {UP: "011", RIGHT: "111", DOWN: "111", LEFT: "110"}))
    BASE_TILES[2].append(Tile("../tile_sets/pcb/6.png",
                           {UP: "111", RIGHT: "121", DOWN: "111", LEFT: "121"}))
    BASE_TILES[2].append(Tile("../tile_sets/pcb/7.png",
                           {UP: "131", RIGHT: "121", DOWN: "131", LEFT: "121"}))
    BASE_TILES[4].append(Tile("../tile_sets/pcb/8.png",
                           {UP: "131", RIGHT: "111", DOWN: "121", LEFT: "111"}))
    BASE_TILES[4].append(Tile("../tile_sets/pcb/9.png",
                           {UP: "121", RIGHT: "121", DOWN: "111", LEFT: "121"}))
    BASE_TILES[2].append(Tile("../tile_sets/pcb/10.png",
                           {UP: "121", RIGHT: "121", DOWN: "121", LEFT: "121"}))
    BASE_TILES[4].append(Tile("../tile_sets/pcb/11.png",
                           {UP: "121", RIGHT: "121", DOWN: "111", LEFT: "111"}))
    BASE_TILES[2].append(Tile("../tile_sets/pcb/12.png",
                           {UP: "111", RIGHT: "121", DOWN: "111", LEFT: "121"}))

def setup_tiles_circles(black_weight = 1, white_weight = 1):
    """
    color definitions:
        black: 0
        white: 1
    :return:
    """
    for _ in range(black_weight):
        BASE_TILES[0].append(Tile("../tile_sets/circles/b.png",
                          {UP: "0", RIGHT: "0", DOWN: "0", LEFT: "0"}))
    BASE_TILES[4].append(Tile("../tile_sets/circles/b_half.png",
                      {UP: "0", RIGHT: "1", DOWN: "1", LEFT: "1"}))
    BASE_TILES[2].append(Tile("../tile_sets/circles/b_i.png",
                      {UP: "0", RIGHT: "1", DOWN: "0", LEFT: "1"}))
    BASE_TILES[4].append(Tile("../tile_sets/circles/b_quarter.png",
                  {UP: "0", RIGHT: "0", DOWN: "1", LEFT: "1"}))

    for _ in range(white_weight):
        BASE_TILES[0].append(Tile("../tile_sets/circles/w.png",
                          {UP: "1", RIGHT: "1", DOWN: "1", LEFT: "1"}))
    BASE_TILES[4].append(Tile("../tile_sets/circles/w_half.png",
                      {UP: "1", RIGHT: "0", DOWN: "0", LEFT: "0"}))
    BASE_TILES[2].append(Tile("../tile_sets/circles/w_i.png",
                      {UP: "1", RIGHT: "0", DOWN: "1", LEFT: "0"}))
    BASE_TILES[4].append(Tile("../tile_sets/circles/w_quarter.png",
                      {UP: "1", RIGHT: "1", DOWN: "0", LEFT: "0"}))

def setup_tiles(tile_set):
    #TODO: Set the tile settings in another class so it is dynamic
    if tile_set == "set1":
        setup_tiles_set1()
    elif tile_set == "pcb":
        setup_tiles_pcb()
    elif tile_set == "circles":
        setup_tiles_circles(TILE_WEIGHTS["black"], TILE_WEIGHTS["white"])
    for num_rotations in BASE_TILES:
        for tile in BASE_TILES[num_rotations]:
            if num_rotations == 0:
                TILES.append(tile)
            else:
                for i in range(num_rotations):
                    rotated_tile = rotate_tile(tile, i)
                    TILES.append(rotated_tile)


def setup():
    global FINISHED_COLLAPSING
    FINISHED_COLLAPSING = False
    setup_tiles(TILE_SET)

    #Set up neighbors for tiles
    for tile in TILES:
        tile.set_neighbors(TILES)

    #Set up grid of cells
    global grid
    grid = [[0 for _ in range(GRID_DIM_HEIGHT)] for _ in range(GRID_DIM_WIDTH)]
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            grid[i][j] = Cell(i, j, TILES)


def draw_tiles():
    if DEBUG: print("drawing\n")
    count = 0
    for row in grid:
        for cell in row:
            cell.draw(DISPLAYSURF)
            count += 1
    if DEBUG: print(f"drew {count} cells!~~~\n")


def collapse_tiles():
    global FINISHED_COLLAPSING

    # 1. Obtain a list of tiles coordinates such that they have the least amount of options
    lowest_entropy = len(TILES)
    lowest_entropy_cells = []
    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            #TODO: Set this up so that we do not need to even look at this tile
            #Perhaps grid is a list of objects with x,y coord
                #or dictionary but i dont think that will work
            #... and when we collapse something, we remove it from the array
            if cell.is_collapsed() or len(cell.options) > lowest_entropy:
                continue
            elif len(cell.options) == lowest_entropy:
                lowest_entropy_cells.append((cell, i, j))
            else:
                lowest_entropy = len(cell.options)
                lowest_entropy_cells = [(cell, i, j)]
    if lowest_entropy_cells:

        # 2. From this list, randomly choose a tile to collapse
        to_collapse_data = random.choice(lowest_entropy_cells)
        cell, x, y = to_collapse_data
        if not cell.collapse():
            print(f"found contradiction in cell ({x},{y})")
            FINISHED_COLLAPSING = True
            return False, x, y

        # 3. Update neighboring tiles using intersection of rules and options
        if x != 0:
            cell_left = grid[x - 1][y]
            cell_left.options = cell_left.options & cell.tile.neighbors[RIGHT]
        if x != GRID_DIM_WIDTH - 1:
            cell_right = grid[x + 1][y]
            cell_right.options = cell_right.options & cell.tile.neighbors[LEFT]
        if y != 0:
            cell_up = grid[x][y - 1]
            cell_up.options = cell_up.options & cell.tile.neighbors[DOWN]
        if y != GRID_DIM_HEIGHT - 1:
            cell_down = grid[x][y + 1]
            cell_down.options = cell_down.options & cell.tile.neighbors[UP]

    else:
        FINISHED_COLLAPSING = True
    return True, None, None

def game_loop():
    global FINISHED_COLLAPSING
    while True:
        #Allow exiting of program with X button
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        #If there remains a single tile not collapsed...
        if not FINISHED_COLLAPSING:
            collapsed, cell_x, cell_y = collapse_tiles()
            if not collapsed:
                print(f"Cannot complete this pattern...")
                print(f"FAIL_CONDITION set to {FAIL_CONDITION}")
                if FAIL_CONDITION == "END":
                    print(f"Ending collapse")
                elif FAIL_CONDITION == "RESET":
                    print(f"Resetting collapse")
                    setup()
                #elif FAIL_CONDITION == "RESET_FROM_FAIL":
                #    print(f"Resetting collapse from failure cell [{cell_x},{cell_y}]")
                #    setup()
                #    grid[cell_x][cell_y].collapse() #doesn't seem to cause the chain reaction i'd expect

        draw_tiles()
        pygame.display.update()
        FramePerSec.tick(FPS)

def get_cell_info():
    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            #print(f"[{i}][{j}] | entropy:{len(cell.options)} | tile: {cell.tile.image_path} | options: {[tile.image_path for tile in cell.options]}")
            print(f"[{i}][{j}] | coordinates:  ")

if __name__ == "__main__":
    pygame.init()
    setup()
    game_loop()