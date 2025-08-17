"""
Frontend for visualization of wave function collapse.
"""
from typing import List
import pygame
import sys
from pygame.locals import *
from app.solver.solver import Solver
from app.solver.node import Node
from app.pygame_frontend.nodesprite import NodeSprite
import configparser


class PygameFrontEnd:
    def __init__(self):
        #Load configuration
        config = configparser.ConfigParser()
        config.read("../../settings.ini")
        self.debug = config.getboolean('debug', 'DEBUG')
        self.solved = False

        #Initialize pygame settings
        pygame.init()
        self.screen_width = int(config['display']['SCREEN_WIDTH'])
        self.screen_height = int(config['display']['SCREEN_HEIGHT'])
        self.display_surf = pygame.display.set_mode((self.screen_width, self.screen_height))
        #self.display_surf = pygame.Surface((self.screen_width, self.screen_height))
        pygame.display.set_caption('Wave Function Collapse')
        self.frame_per_sec = pygame.time.Clock()
        self.fps = int(config['pygame']['FPS'])

        #Initialize grid, sprites, tiles, and prepare for solving
        self.solver = Solver(debug=self.debug)
        self.sprite_group = self.setup_sprites(self.solver.get_grid(), self.screen_width, self.screen_height)


    def setup_sprites(self, grid: List[List[Node]], width, height) -> pygame.sprite.Group:
        """Sets up sprite group for rendering wave function collapse using pygame engine."""
        if self.debug: print("setting up sprites...")
        sprite_width = width // len(grid)
        sprite_height = height // len(grid[0])
        sprites = pygame.sprite.Group()
        for i, row in enumerate(grid):
            for j, node in enumerate(row):
                sprites.add(NodeSprite(i, j, node, sprite_width, sprite_height, debug=self.debug))
        return sprites

    def solve_wave(self):
        #Solve the wave
        print("Solving...")
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
            if not self.solved:
                self.solve_next()

            #Update gui after each step
            self.frame_per_sec.tick(self.fps)
            pygame.display.flip()

    def solve_next(self):
        if not self.solver.is_solved():
            if self.solver.solve_next():
                self.sprite_group.update()
                self.sprite_group.draw(self.display_surf)
            elif self.solver.fail_condition == "RESET" or self.solver.fail_condition == "RESET_FROM_FAIL":
                self.sprite_group = self.setup_sprites(self.solver.get_grid(),
                                                       self.screen_width, self.screen_height)
        else:
            self.solved = True
            if self.debug: print("Solved!")


if __name__ == "__main__":
    frontend = PygameFrontEnd()
    frontend.solve_wave()