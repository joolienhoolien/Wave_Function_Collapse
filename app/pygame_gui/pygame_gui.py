import pygame
import sys
from pygame.locals import *
from app.solver.solver import Solver
from nodesprite import NodeSprite
import configparser

CONFIG = configparser.ConfigParser()
CONFIG.read('../../settings.ini')
SCREEN_WIDTH = int(CONFIG['display']['SCREEN_WIDTH'])
SCREEN_HEIGHT = int(CONFIG['display']['SCREEN_HEIGHT'])
SPRITE_WIDTH = int(CONFIG['display']['SCREEN_WIDTH']) // int(CONFIG['grid']['GRID_DIM_WIDTH'])
SPRITE_HEIGHT = int(CONFIG['display']['SCREEN_HEIGHT']) // int(CONFIG['grid']['GRID_DIM_HEIGHT'])
DEBUG = CONFIG.getboolean('debug','DEBUG')
FramePerSec = pygame.time.Clock()
FPS = 60
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
SPRITE_GROUP = pygame.sprite.Group()

def setup_sprites(grid):
    for i, row in enumerate(grid):
        for j, node in enumerate(row):
            SPRITE_GROUP.add(NodeSprite(i, j, node, SPRITE_WIDTH, SPRITE_HEIGHT, debug=DEBUG))


if __name__ == "__main__":
    pygame.init()
    #Any intro gui options go here
    #Maybe you click "solve puzzle!" then it goes to the following code...
    #Step 1 and 2 - create tiles and a grid
    if DEBUG: print("Starting...")
    solver = Solver(debug=DEBUG)
    if DEBUG: print("setting up sprites array...")
    setup_sprites(solver.get_grid())

    #Step 3 goes here, any adjustments on the front end before running...
    #Step 4, solve!
    if DEBUG: print("Solving...")
    while True: #Can change the "True" to a setting...
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        if not solver.is_solved():
            if solver.solve_next():
                SPRITE_GROUP.update()
                SPRITE_GROUP.draw(DISPLAYSURF)
        else:
            if DEBUG: print("Solved!")
        pygame.display.flip()
        FramePerSec.tick(FPS)
    #can have other solver methods for slower solving potentially.
        #or just other arguments in the solve method
    #Step 5... anything we want to do like save to file or go back to step 1 or whatever