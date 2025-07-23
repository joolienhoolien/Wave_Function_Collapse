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

from PIL import Image

from app.tile import Tile
from settings import *

#or pass in "all_options" in constructor and assert it's populated
def get_average_image(tiles = None, name=None):
    if tiles:
        global DEFAULT_TILE
        #Get filepath
    #    ext = os.path.splitext(tile_types[0].image_path)[1]
    #    filepath = f"../tile_temp/{name}_{TILE_SET}{ext}"

        #If we already generated this tile... return tiles image
        if name == "DEFAULT" and type(DEFAULT_TILE) is Tile:
            return DEFAULT_TILE.image

        #Generate average image
        averaged_image = tiles[0].image
        for i, tile in enumerate(tiles):
            if i == 0: continue
            image = tile.image
            averaged_image = Image.blend(averaged_image, image, 1.0/float(i))

        #If we intend to use this as our default tile, save it for future reference
        if name == "DEFAULT":
            DEFAULT_TILE = Tile(image=averaged_image)
        return averaged_image
    else:
        return None


class Cell(pygame.sprite.Sprite):
    def __init__(self, i, j, tile_types):
        super().__init__()

        width = SCREEN_WIDTH / GRID_DIM_WIDTH
        x_center = width / 2
        x = x_center + (width * i)

        height = SCREEN_HEIGHT / GRID_DIM_HEIGHT
        y_center = height / 2
        y = y_center + (height * j)

        #Tile information
        self.collapsed = False
        self.possible_neighbors = set(tile_types)
        self.average_image = get_average_image(tiles=tile_types, name="DEFAULT")
        self.tile = self.average_image

        #Image information
        self.x, self.y = x, y
        self.sprite_width = width
        self.sprite_height = height
        #self.image = self.average_image.load
        self.image = pygame.image.fromstring(self.average_image.tobytes(), self.average_image.size, self.average_image.mode).convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.sprite_width, self.sprite_height))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update_options(self, options):
        #Update the options
        self.possible_neighbors = options

        #Update the image based on remaining options
        #filename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        average_image = get_average_image(tiles= list(options))
        self.update_image(image=average_image)


    def is_collapsed(self) -> bool:
        return self.collapsed

    def collapse(self):
        if not self.possible_neighbors:
            return False
        else:
            self.update_tile(tile=random.choice(tuple(self.possible_neighbors)))
            return True

    def update_tile(self, tile):
        self.collapsed = True
        self.possible_neighbors = set()
        self.update_image(tile.image)
        self.tile = tile

    def update_image(self, image, **kwargs):
        width = kwargs.get('width', self.sprite_width)
        height = kwargs.get('height', self.sprite_height)
        self.image = pygame.image.fromstring(image.tobytes(), image.size, image.mode).convert_alpha()
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect.center = (self.x, self.y)

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        if DEBUG: print(f"Drawing cell [{self.x}, {self.y}]")

