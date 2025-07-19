import sys
import pygame
from pygame.locals import *

#Color reference
BLACK = pygame.Color(0,0,0)
WHITE = pygame.Color(255,255,255)
GREY = pygame.Color(128,128,128)
RED = pygame.Color(255,0,0)
GREEN = pygame.Color(0,255,0)
BLUE = pygame.Color(0,0,255)

#Display
SCREEN_WIDTH, SCREEN_HEIGHT = 100, 100
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
DISPLAYSURF.fill(WHITE)

#Frames
FramePerSec = pygame.time.Clock()
FPS = 60

#Grid stuff
grid_dim = 2
grid = []
tiles = ["../tiles/blank.png",
         "../tiles/up.png",
         "../tiles/right.png",
         "../tiles/down.png",
         "../tiles/left.png",]
BLANK, UP, RIGHT, DOWN, LEFT = 0, 1, 2, 3, 4

class Tile(pygame.sprite.Sprite):
    collapsed = False
    options = [BLANK, UP, RIGHT, DOWN, LEFT]
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
        self.options = [value]
        self.image = pygame.image.load(tiles[value])


def setup():
    global grid
    grid = [[0 for _ in range(grid_dim)] for _ in range(grid_dim)]
    for i in range(grid_dim):
        for j in range(grid_dim):
            tile_width = SCREEN_WIDTH / grid_dim
            tile_x_center = tile_width / 2
            x = tile_x_center + (tile_width * i)

            tile_width = SCREEN_WIDTH / grid_dim
            tile_y_center = tile_width / 2
            y = tile_y_center + (tile_width * j)

            grid[i][j] = Tile(x, y, BLANK)



def game_loop():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        for row in grid:
            for tile in row:
                tile.draw(DISPLAYSURF)
        pygame.display.update()
        FramePerSec.tick(FPS)


if __name__ == "__main__":
    pygame.init()
    setup()
    #grid[1][0].set_value(LEFT) #manually collapsing cell for testing
    game_loop()