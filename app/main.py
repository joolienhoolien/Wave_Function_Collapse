import sys
import pygame
from pygame.locals import *
import random
from tile import Tile
from cell import Cell

#Color reference
BLACK = pygame.Color(0,0,0)
WHITE = pygame.Color(255,255,255)
GREY = pygame.Color(128,128,128)
RED = pygame.Color(255,0,0)
GREEN = pygame.Color(0,255,0)
BLUE = pygame.Color(0,0,255)

#Display
SCREEN_WIDTH, SCREEN_HEIGHT = 1000,1000
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
#DISPLAYSURF.fill(GREEN)

#Frames
FramePerSec = pygame.time.Clock()
FPS = 60

#Grid
GRID_DIM = 20
grid = []

#Tiles
TILE_IMAGES = ["../tiles/blank.png",
         "../tiles/up.png",
         "../tiles/right.png",
         "../tiles/down.png",
         "../tiles/left.png", ]
BLANK, UP, RIGHT, DOWN, LEFT = 0, 1, 2, 3, 4
ALL_OPTIONS = {BLANK, UP, RIGHT, DOWN, LEFT}
FINISHED_COLLAPSING = False
SPRITE_SIZE_W, SPRITE_SIZE_H = SCREEN_WIDTH // GRID_DIM, SCREEN_HEIGHT // GRID_DIM
TILES = []
#print(SPRITE_SIZE_W, SPRITE_SIZE_H)

def setup():
    #Set up base tiles
    TILES.append(Tile("../tiles/blank.png",
                      {UP: {0}, RIGHT: {0}, DOWN: {0}, LEFT: {0}}))
    TILES.append(Tile("../tiles/up.png",
                      {UP: {1}, RIGHT: {1}, DOWN: {0}, LEFT: {1}}))
    TILES.append(Tile("../tiles/right.png",
                      {UP: {1}, RIGHT: {1}, DOWN: {1}, LEFT: {0}}))
    TILES.append(Tile("../tiles/down.png",
                      {UP: {0}, RIGHT: {1}, DOWN: {1}, LEFT: {1}}))
    TILES.append(Tile("../tiles/left.png",
                      {UP: {1}, RIGHT: {0}, DOWN: {1}, LEFT: {1}}))
    #TODO: Add rotating to set up alt tiles

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