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
import random
import pygame

#TODO: Import from settings.py and have a field for "ALL_OPTIONS"
#TODO: Have default tile also in here

#or pass in "all_options" in constructor and assert it's populated
class Cell(pygame.sprite.Sprite):
    def __init__(self, x, y, tile_types, width, height):
        super().__init__()
        #Tile information
        self.collapsed = False
        self.options = set(tile_types)
        self.default_tile = tile_types[0]
        self.tile = self.default_tile

        #Image information
        self.x, self.y = x, y
        self.sprite_width = width
        self.sprite_height = height
        self.image = pygame.image.load(self.default_tile.image_path).convert_alpha()
        #TODO: I think the bug about the images being drawn funny is in this line
        self.image = pygame.transform.scale(self.image, (self.sprite_width, self.sprite_height))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def collapse(self):
        #TODO: the class above needs to handle which tile we collapse into
        if not self.options:
            self.update_tile(self.default_tile) #TODO how to handle default tile?
        else:
            self.update_tile(random.choice(tuple(self.options)))

    def update_tile(self, tile):
        self.collapsed = True
        self.options = set()
        self.update_image(tile.image_path)
        self.tile = tile

    def update_image(self, image_path: str, **kwargs):
        width = kwargs.get('width', self.sprite_width)
        height = kwargs.get('height', self.sprite_height)
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect.center = (self.x, self.y)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

