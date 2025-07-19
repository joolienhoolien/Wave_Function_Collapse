import sys
import pygame
from pygame.locals import *
import random

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
DISPLAYSURF.fill(WHITE)

#Frames
FramePerSec = pygame.time.Clock()
FPS = 60

#Grid
GRID_DIM = 20
grid = []

#Tiles
tiles = ["../tiles/blank.png",
         "../tiles/up.png",
         "../tiles/right.png",
         "../tiles/down.png",
         "../tiles/left.png",]
BLANK, UP, RIGHT, DOWN, LEFT = 0, 1, 2, 3, 4
ALL_OPTIONS = {BLANK, UP, RIGHT, DOWN, LEFT}
TILE_RULES = {
    BLANK: {UP : {BLANK, UP},
            RIGHT: {BLANK, RIGHT},
            DOWN: {BLANK, DOWN},
            LEFT: {BLANK, LEFT}
            },
    UP: {UP : {RIGHT, DOWN, LEFT},
         RIGHT: {UP, DOWN, LEFT},
         DOWN: {BLANK, DOWN},
         LEFT: {DOWN, RIGHT, UP}
         },
    RIGHT: {UP : {RIGHT, DOWN, LEFT},
         RIGHT: {UP, DOWN, LEFT},
         DOWN: {UP, RIGHT, LEFT},
         LEFT: {BLANK, LEFT}
            },
    DOWN: {UP : {BLANK, UP},
         RIGHT: {UP, DOWN, LEFT},
         DOWN: {LEFT, RIGHT, UP},
         LEFT: {UP, RIGHT, DOWN}
           },
    LEFT: {UP : {LEFT, DOWN, RIGHT},
         RIGHT: {BLANK, RIGHT},
         DOWN: {LEFT, RIGHT, UP},
         LEFT: {DOWN, RIGHT, UP}
           },
}

FINISHED_COLLAPSING = False


class Tile(pygame.sprite.Sprite):
    collapsed = False
    options = {BLANK, UP, RIGHT, DOWN, LEFT}
    value = BLANK

    def __init__(self, x, y, tile):
        super().__init__()
        self.image = pygame.image.load(tiles[tile])
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def set_value(self, value):
        self.value = value
        self.collapsed = True
        self.options = set()
        self.image = pygame.image.load(tiles[value])

    def collapse(self):
        if not self.options:
            self.set_value(BLANK)
        else:
            self.set_value(random.choice(tuple(self.options)))


def setup():
    global grid
    grid = [[0 for _ in range(GRID_DIM)] for _ in range(GRID_DIM)]
    for i in range(GRID_DIM):
        for j in range(GRID_DIM):
            tile_width = SCREEN_WIDTH / GRID_DIM
            tile_x_center = tile_width / 2
            x = tile_x_center + (tile_width * i)

            tile_width = SCREEN_WIDTH / GRID_DIM
            tile_y_center = tile_width / 2
            y = tile_y_center + (tile_width * j)

            grid[i][j] = Tile(x, y, BLANK)


def draw_tiles():
    for row in grid:
        for tile in row:
            tile.draw(DISPLAYSURF)


def collapse_tiles():
    global FINISHED_COLLAPSING
    # Calculate which is the next tile to collapse
    # 1. Obtain a list of tiles coordinates such that they have the least amount of options
    lowest_num_options = len(ALL_OPTIONS)
    lowest_entropy = []
    for i, row in enumerate(grid):
        for j, tile in enumerate(row):
            if tile.collapsed or len(tile.options) > lowest_num_options:
                continue
            elif len(tile.options) == lowest_num_options:
                lowest_entropy.append((tile, i, j))
            else:
                lowest_num_options = len(tile.options)
                lowest_entropy = [(tile, i, j)]
    if lowest_entropy:

        # 2. From this list, randomly choose a tile to collapse
        to_collapse_data = random.choice(lowest_entropy)
        tile, x, y = to_collapse_data
        tile.collapse()
        print(f"Collapsing tile at grid[{x},{y}] into {tile.value}")

        # 3. Update neighboring tiles using intersection of rules and options
        if x != 0:
            tile_left = grid[x - 1][y]
            print(f"Looking at neighbor UP... ({x - 1}, {y}), options={tile_left.options}")
            tile_left.options = tile_left.options & TILE_RULES[tile.value][LEFT]
            print(f"After update... ({x - 1}, {y}), options={tile_left.options}")
        if x != GRID_DIM - 1:
            tile_right = grid[x + 1][y]
            print(f"Looking at neighbor DOWN... ({x + 1}, {y}), options={tile_right.options}")
            tile_right.options = tile_right.options & TILE_RULES[tile.value][RIGHT]
            print(f"After update... ({x + 1}, {y}), options={tile_right.options}")
        if y != 0:
            tile_up = grid[x][y - 1]
            print(f"Looking at neighbor LEFT... ({x}, {y - 1}), options={tile_up.options}")
            tile_up.options = tile_up.options & TILE_RULES[tile.value][UP]
            print(f"After update... ({x}, {y - 1}), options={tile_up.options}")
        if y != GRID_DIM - 1:
            tile_down = grid[x][y + 1]
            #print(f"Looking at neighbor RIGHT... ({x}, {y + 1}), options={tile_down.options}")
            tile_down.options = tile_down.options & TILE_RULES[tile.value][DOWN]
            #print(f"After update... ({x}, {y + 1}), options={tile_down.options}")

    else:
        FINISHED_COLLAPSING = True

def game_loop():
    global FINISHED_COLLAPSING
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        #If there remains a single tile not collapsed...
        if not FINISHED_COLLAPSING:
            print("\n\nCollapsing tiles...")
            collapse_tiles()

        draw_tiles()
        pygame.display.update()
        FramePerSec.tick(FPS)


if __name__ == "__main__":
    pygame.init()
    setup()
    game_loop()