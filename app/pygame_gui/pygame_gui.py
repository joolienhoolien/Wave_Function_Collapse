"""
GUI for interacting with wave function collapse backend.
"""

from typing import List
import pygame
import sys
from pygame.locals import *
from app.solver.solver import Solver
from app.solver.node import Node
from nodesprite import NodeSprite
import configparser


def setup_sprites(grid: List[List[Node]], width, height, debug=False) -> pygame.sprite.Group:
    """Sets up sprite group for rendering wave function collapse using pygame engine."""
    if debug: print("setting up sprites...")
    sprite_width = width // len(grid)
    sprite_height = height // len(grid[0])
    sprites = pygame.sprite.Group()
    for i, row in enumerate(grid):
        for j, node in enumerate(row):
            sprites.add(NodeSprite(i, j, node, sprite_width, sprite_height, debug=debug))
    return sprites


if __name__ == "__main__":
    #Load configuration
    config = configparser.ConfigParser()
    config.read('../../settings.ini')
    debug = config.getboolean('debug', 'DEBUG')

    #Initialize pygame settings
    pygame.init()
    screen_width = int(config['display']['SCREEN_WIDTH'])
    screen_height = int(config['display']['SCREEN_HEIGHT'])
    display_surf = pygame.display.set_mode((screen_width, screen_height))
    frame_per_sec = pygame.time.Clock()
    fps = int(config['pygame']['FPS'])

    #TODO: Intro GUI

    #Initialize grid, sprites, tiles, and prepare for solving
    solver = Solver(debug=debug)
    sprite_group = setup_sprites(solver.get_grid(), screen_width, screen_height)

    #Solve the wave
    if debug: print("Solving...")
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        if not solver.is_solved():
            if solver.solve_next():
                sprite_group.update()
                sprite_group.draw(display_surf)
            elif solver.fail_condition == "RESET" or solver.fail_condition == "RESET_FROM_FAIL":
                #solver.reset()
                sprite_group = setup_sprites(solver.get_grid(), screen_width, screen_height)
        else:
            if debug: print("Solved!")

        #Update gui after each step
        pygame.display.flip()
        frame_per_sec.tick(fps)

    #TODO: Save the file, run again, etc