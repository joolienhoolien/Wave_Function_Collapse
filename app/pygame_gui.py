import pygame
import sys
from pygame.locals import *
from solver import Solver


DEBUG = True
FramePerSec = pygame.time.Clock()
FPS = 60
SCREEN_WIDTH = 16 * 100
SCREEN_HEIGHT = 9 * 100
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
Cells = []


def draw_tiles(s: Solver):
    if DEBUG: print("drawing\n")
    count = 0
    for row in s.grid.grid:
        for node in row:
            node.draw(DISPLAYSURF)
            count += 1
    if DEBUG: print(f"drew {count} cells!~~~\n")


if __name__ == "__main__":
    pygame.init()
    #Any intro gui options go here
    #Maybe you click "solve puzzle!" then it goes to the following code...
    #Step 1 and 2 - create tiles and a grid
    solver = Solver()

    #Step 3 goes here, any adjustments on the front end before running...
    #Step 4, solve!
    while True: #Can change the "True" to a setting...
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        solver.solve_next()
        draw_tiles(solver)
        pygame.display.update()
        FramePerSec.tick(FPS)
    #can have other solver methods for slower solving potentially.
        #or just other arguments in the solve method
    #Step 5... anything we want to do like save to file or go back to step 1 or whatever