import pygame
import sys
from pygame.locals import *
from solver import Solver
from nodesprite import NodeSprite
from settings import *

FramePerSec = pygame.time.Clock()
FPS = 60
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
SPRITES = []


def draw_sprites():
    if DEBUG: print("drawing\n")
    count = 0
    for row in SPRITES:
        for sprite in row:
            sprite.draw(DISPLAYSURF)
            count += 1
    if DEBUG: print(f"drew {count} cells!~~~\n")

def update_sprites(grid_of_sprites):
    for i, _ in enumerate(SPRITES):
        for j, sprite in enumerate(SPRITES[i]):
            sprite.update_image(list(grid_of_sprites[i][j].get_tile_options()))

def setup_sprites(grid_of_sprites):
    return [[NodeSprite(i, j, list(node.get_tile_options())) for j,node in enumerate(grid_of_sprites[i])] for i,_ in enumerate(grid_of_sprites)]


if __name__ == "__main__":
    pygame.init()
    #Any intro gui options go here
    #Maybe you click "solve puzzle!" then it goes to the following code...
    #Step 1 and 2 - create tiles and a grid
    if DEBUG: print("Starting...")
    solver = Solver()
    if DEBUG: print("setting up sprites array...")
    SPRITES = setup_sprites(solver.get_grid())

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
                update_sprites(solver.get_grid())
                draw_sprites()
        else:
            if DEBUG: print("Solved!")
        pygame.display.update()
        FramePerSec.tick(FPS)
    #can have other solver methods for slower solving potentially.
        #or just other arguments in the solve method
    #Step 5... anything we want to do like save to file or go back to step 1 or whatever