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
import pygame
from pygame.locals import *
import random
from tile import Tile, rotate_tile
from cell import Cell

#Display
SCREEN_WIDTH, SCREEN_HEIGHT = 800,800
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
#DISPLAYSURF.fill(GREEN)

#Frames
FramePerSec = pygame.time.Clock()
FPS = 60

#Grid
GRID_DIM = 50
grid = []

#Tiles
BLANK, UP, RIGHT, DOWN, LEFT = 0, 1, 2, 3, 4
ALL_OPTIONS = {BLANK, UP, RIGHT, DOWN, LEFT}
FINISHED_COLLAPSING = False
SPRITE_SIZE_W, SPRITE_SIZE_H = SCREEN_WIDTH // GRID_DIM, SCREEN_HEIGHT // GRID_DIM
TILES = []
BASE_TILES = []


def setup_tiles_set1():
    #Blank tile is a special case
    TILES.append(Tile("../tile_sets/set1/blank.png",
                      {UP: {0}, RIGHT: {0}, DOWN: {0}, LEFT: {0}}))
    #Set up base tiles
    BASE_TILES.append(Tile("../tile_sets/set1/T.png",
                           {UP: {1}, RIGHT: {1}, DOWN: {0}, LEFT: {1}}))

def setup_tiles_pcb():
    """
    side definitions:
        GREY: 0
        GREEN: 1
        LIGHT GREEN CONNECTOR: 2
        LIGHT GREY CONNECTOR: 3
        GREY THEN GREEN: 4
        GREEN THEN GREY: 5
    :return:
    """
    #Full Green
    TILES.append(Tile("../tile_sets/pcb/1.png",
                      {UP: {1}, RIGHT: {1}, DOWN: {1}, LEFT: {1}}))
    #Full Grey
    TILES.append(Tile("../tile_sets/pcb/0.png",
                      {UP: {0}, RIGHT: {0}, DOWN: {0}, LEFT: {0}}))

    #Set up base tiles
    BASE_TILES.append(Tile("../tile_sets/pcb/2.png",
                           {UP: {1}, RIGHT: {2}, DOWN: {1}, LEFT: {1}}))
    BASE_TILES.append(Tile("../tile_sets/pcb/3.png",
                           {UP: {1}, RIGHT: {3}, DOWN: {1}, LEFT: {3}}))
    #BASE_TILES.append(Tile("../tile_sets/pcb/4.png",
    #                       {UP: {4}, RIGHT: {2}, DOWN: {5}, LEFT: {0}}))
    #BASE_TILES.append(Tile("../tile_sets/pcb/5.png",
    #                       {UP: {4}, RIGHT: {1}, DOWN: {1}, LEFT: {5}}))
    BASE_TILES.append(Tile("../tile_sets/pcb/6.png",
                           {UP: {1}, RIGHT: {2}, DOWN: {1}, LEFT: {2}}))
    BASE_TILES.append(Tile("../tile_sets/pcb/7.png",
                           {UP: {3}, RIGHT: {2}, DOWN: {3}, LEFT: {2}}))
    BASE_TILES.append(Tile("../tile_sets/pcb/8.png",
                           {UP: {3}, RIGHT: {1}, DOWN: {2}, LEFT: {1}}))
    BASE_TILES.append(Tile("../tile_sets/pcb/9.png",
                           {UP: {2}, RIGHT: {2}, DOWN: {1}, LEFT: {2}}))
    BASE_TILES.append(Tile("../tile_sets/pcb/10.png",
                           {UP: {2}, RIGHT: {2}, DOWN: {2}, LEFT: {2}}))
    BASE_TILES.append(Tile("../tile_sets/pcb/11.png",
                           {UP: {2}, RIGHT: {2}, DOWN: {1}, LEFT: {1}}))
    BASE_TILES.append(Tile("../tile_sets/pcb/12.png",
                           {UP: {1}, RIGHT: {2}, DOWN: {1}, LEFT: {2}}))


def setup_tiles(tile_set):
    #TODO: Set the tile settings in another class so it is dynamic
    if tile_set == "set1":
        setup_tiles_set1()
    elif tile_set == "pcb":
        setup_tiles_pcb()
    for tile in BASE_TILES:
        for i in range(4): #TODO: Some tiles I only want to rotate once i.e. they are same if you 180 rotate them
            rotated_tile = rotate_tile(tile, i)
            TILES.append(rotated_tile)


def setup():
    setup_tiles("pcb")

    #Set up neighbors for tiles
    for tile in TILES:
        tile.set_neighbors(TILES)

    #Set up grid of cells
    global grid
    grid = [[0 for _ in range(GRID_DIM)] for _ in range(GRID_DIM)]
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            cell_width = SCREEN_WIDTH / GRID_DIM
            cell_x_center = cell_width / 2
            x = cell_x_center + (cell_width * i)

            cell_width = SCREEN_WIDTH / GRID_DIM
            cell_y_center = cell_width / 2
            y = cell_y_center + (cell_width * j)

            grid[i][j] = Cell(x, y, TILES, SPRITE_SIZE_W, SPRITE_SIZE_H)
            #print(x,y)


def draw_tiles():
    #TODO: Bug with drawing tiles too many times? Think I saw this loop too much in debugging earlier in dev
    for row in grid:
        for cell in row:
            cell.draw(DISPLAYSURF)


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
            if cell.collapsed or len(cell.options) > lowest_entropy:
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
        cell.collapse()

        # 3. Update neighboring tiles using intersection of rules and options
        if x != 0:
            cell_left = grid[x - 1][y]
            cell_left.options = cell_left.options & cell.tile.neighbors[RIGHT]
        if x != GRID_DIM - 1:
            cell_right = grid[x + 1][y]
            cell_right.options = cell_right.options & cell.tile.neighbors[LEFT]
        if y != 0:
            cell_up = grid[x][y - 1]
            cell_up.options = cell_up.options & cell.tile.neighbors[DOWN]
        if y != GRID_DIM - 1:
            cell_down = grid[x][y + 1]
            cell_down.options = cell_down.options & cell.tile.neighbors[UP]

    else:
        FINISHED_COLLAPSING = True

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
            collapse_tiles()

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