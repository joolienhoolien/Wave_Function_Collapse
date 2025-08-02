
import pygame


class NodeSprite(pygame.sprite.Sprite):
    """
    Extension of pygame.sprite.Sprite. An individual sprite in the full group of sprites. Represents a single node.:
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
    def __init__(self, i, j, node, width, height, debug=False):
        """Visual representation of a node.
        State:
            node: reference to a node
            x, y: coordinate on the screen given screen and grid dimensions
            sprite_width, sprite_height: size of the sprite on the screen
            images: list of potential images representing the node. Once collapsed, list will be length = 1
            image: average image given list of all images
            rect: rectangle around the visual for rendering purposes
            rect.center: center of the visual for rendering purposes"""
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
        """
        Updates the sprite image if it needs to be updated based on the state of the node it represents.
        Returns:
             None
        """
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
        """
        Draw the sprite's image to the surface
        :param surface:
        :return:
        """
        surface.blit(self.image)
        if self.debug: print(f"Drawing cell [{self.x}, {self.y}]")

