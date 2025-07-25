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


class NodeSprite(pygame.sprite.Sprite):
    def __init__(self, i, j, node, width, height, debug=False):
        super().__init__()
        self.node = node
        self.debug = debug

        self.x = (width / 2) + (width * i)
        self.y = (height / 2) + (height * j)

        self.sprite_width = width
        self.sprite_height = height

        #All possible image states
        self.images = []
        for tile_option in node.get_tile_options():
            image = pygame.image.load(tile_option.image_path).convert_alpha()
            image = pygame.transform.scale(image, (self.sprite_width, self.sprite_height))
            image = pygame.transform.rotate(image, -90 * tile_option.rotations)
            self.images.append(image)
        self.image = pygame.transform.average_surfaces(self.images)

        #Positioning
        self.rect = self.images[0].get_rect()
        self.rect.center = (self.x, self.y)

    def update(self):
        if self.node.get_reset_updated():
            if len(self.node.tile_options) == 0: return
            self.images = []
            for tile_option in self.node.tile_options:
                image = pygame.image.load(tile_option.image_path).convert_alpha()
                image = pygame.transform.scale(image, (self.sprite_width, self.sprite_height))
                image = pygame.transform.rotate(image, -90 * tile_option.rotations)
                self.images.append(image)
            self.image = pygame.transform.average_surfaces(self.images)

            #Positioning
            self.rect = self.images[0].get_rect()
            self.rect.center = (self.x, self.y)

    def draw(self, surface):
        surface.blit(self.image)
        if self.debug: print(f"Drawing cell [{self.x}, {self.y}]")

