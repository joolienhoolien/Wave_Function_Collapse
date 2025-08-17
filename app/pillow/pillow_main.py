import configparser

from PIL import Image
from app.solver.solver import Solver

if __name__ == '__main__':
    solver = Solver()
    grid_width, grid_height = solver.get_grid_dimensions()
    config = configparser.ConfigParser()
    config.read("../../settings.ini")
    screen_width = int(config['display']['SCREEN_WIDTH'])
    screen_height = int(config['display']['SCREEN_HEIGHT'])
    node_width = screen_width // grid_width
    node_height = screen_height // grid_height
    grid_image = Image.new("RGB", (screen_width, screen_height), "white")
    while not solver.is_solved():
        solver.solve_next()
    grid = solver.get_grid()

    for row in grid:
        for node in row:
            #Create a combination image of all the tile options
            options = list(node.tile_options)
            blended_image = Image.open(options[0].image_path).resize((node_width, node_height))
            blended_image = blended_image.rotate(-90 * options[0].rotations)
            for k in range(1, len(options)):
                option = options[k]
                node_image = Image.open(option.image_path).resize((node_width, node_height))
                node_image = node_image.rotate(-90 * option.rotations)

                #Blend image
                alpha = 1.0 / (k + 1)
                blended_image = Image.blend(blended_image, node_image, alpha)

            #Place the blended image in its corresponding location
            grid_image.paste(blended_image, (node_width * node.x, node_height * node.y))
    grid_image.show() #TODO: Return this image or something else for launcher to use
