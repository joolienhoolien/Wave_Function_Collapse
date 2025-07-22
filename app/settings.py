import pygame

#DEBUG
DEBUG = False

#Contradiction
"""
FAIL_CONDITIONS are to direct the program what to do in case the wave collapses such that a contradiction is created.
 A contradiction occurs when there is a cell with no possible tiles, and would only result in an improper image.
 Options for FAIL_CONDITION: 
    - "END" - end the program and print to command line.
    - "RESET" - reset the board and try again at a random cell.
    - NOT IMPLEMENTED "RESET_FROM_FAIL" - reset the board to default and rerun, starting from the failed cell.
    - NOT IMPLEMENTED "BACKTRACK" - move backwards from the failure point and try new combinations
"""

FAIL_CONDITION = "RESET"

#Display
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
#DISPLAYSURF.fill(GREEN)

#Grid
GRID_DIM_WIDTH = 50
GRID_DIM_HEIGHT = 50

#Frames
FramePerSec = pygame.time.Clock()
FPS = 60

#Tiles
BLANK, UP, RIGHT, DOWN, LEFT = 0, 1, 2, 3, 4
ALL_OPTIONS = {BLANK, UP, RIGHT, DOWN, LEFT}
SPRITE_SIZE_W, SPRITE_SIZE_H = SCREEN_WIDTH // GRID_DIM_WIDTH, SCREEN_HEIGHT // GRID_DIM_HEIGHT
TILE_SET = "circles"
TILE_WEIGHTS = {"black": 500, "white": 1}