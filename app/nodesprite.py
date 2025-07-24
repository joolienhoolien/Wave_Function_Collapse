"""
Cell class responsibilities:
    - Instantiation of a cell with information given from a type of tile
        - Draw to the surface
            - Screen coordinates
                - Image size details
            - Image once collapsed, image before collapse
                - Convention to have the 0th tile be the default tile.
        - Hold onto a set of valid pieces we can place on it "options"
        - Reduce the set of valid pieces given a set of a neighbor and direction of neighbor
        - Collapse
            - Set an image given the tile we choose
            - Reduce options to empty set
            - Mark as collapsed
"""
import pygame

from settings import *


class NodeSprite(pygame.sprite.Sprite):
    def __init__(self, i, j, tile_options):
        super().__init__()

        width = SCREEN_WIDTH / GRID_DIM_WIDTH
        x_center = width / 2
        x = x_center + (width * i)

        height = SCREEN_HEIGHT / GRID_DIM_HEIGHT
        y_center = height / 2
        y = y_center + (height * j)

        self.sprite_width = width
        self.sprite_height = height

        #All possible image states
        self.images = []
        for tile_option in tile_options:
            image = pygame.image.load(tile_option.image_path).convert_alpha()
            image = pygame.transform.scale(image, (self.sprite_width, self.sprite_height))
            image = pygame.transform.rotate(image, -90 * tile_option.rotations)
            self.images.append(image)

        #Positioning
        self.rect = self.images[0].get_rect()
        self.x, self.y = x, y
        self.rect.center = (x, y)

    def update(self, tile_options):
        if len(tile_options) == 0: return
        self.images = []
        for tile_option in tile_options:
            image = pygame.image.load(tile_option.image_path).convert_alpha()
            image = pygame.transform.scale(image, (self.sprite_width, self.sprite_height))
            image = pygame.transform.rotate(image, -90 * tile_option.rotations)
            self.images.append(image)

        #Positioning
        self.rect = self.images[0].get_rect()
        self.rect.center = (self.x, self.y)

    def draw(self, surface):
        if len(self.images) == 1:
            surface.blit(self.images[0], self.rect)
        else:
            image = pygame.transform.average_surfaces(self.images)
            surface.blit(image, self.rect)
        if DEBUG: print(f"Drawing cell [{self.x}, {self.y}]")

