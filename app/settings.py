#DEBUG
DEBUG = False

#Contradiction
"""
FAIL_CONDITIONS are to direct the program what to do in case the wave collapses such that a contradiction is created.
 A contradiction occurs when there is a cell with no possible tiles, and would only result in an improper image.
 Options for FAIL_CONDITION: 
    - "END" - end the program and print to command line.
    - NOT IMPLEMENTED "RESET" - reset the board and try again at a random cell.
    - NOT IMPLEMENTED "RESET_FROM_FAIL" - reset the board to default and rerun, starting from the failed cell.
    - NOT IMPLEMENTED "BACKTRACK" - move backwards from the failure point and try new combinations
"""

FAIL_CONDITION = "END"

#Display
SCREEN_WIDTH = 16 * 100
SCREEN_HEIGHT = 9 * 100

#Grid
GRID_DIM_WIDTH = 16 * 10
GRID_DIM_HEIGHT = 9 * 10

#Tiles
BLANK, UP, RIGHT, DOWN, LEFT = 0, 1, 2, 3, 4
#TILE_CONVERSION = {"UP" : 1, "RIGHT" : 2, "DOWN" : 3, "LEFT" : 4}
ALL_OPTIONS = {BLANK, UP, RIGHT, DOWN, LEFT}
SPRITE_SIZE_W, SPRITE_SIZE_H = SCREEN_WIDTH // GRID_DIM_WIDTH, SCREEN_HEIGHT // GRID_DIM_HEIGHT
TILE_SET = "circles"
TILE_WEIGHTS = {"black": 1, "white": 1}
TILE_SET_FILEPATH_BASE = f"../base_tiles/{TILE_SET}/"
TILE_SET_JSON = f"{TILE_SET_FILEPATH_BASE}{TILE_SET}.json"
DEFAULT_TILE = None
