"""
Responsible for:
    - Settings (grid dimensions, fail condition, tile_set)
    - Creating and managing the grid
"""
from grid import Grid
import configparser


def get_json_path(config):
    base_path = f"../{config['tiles']['TILE_SET_FOLDER']}"
    tile_set_name = config["tiles"]["TILE_SET_NAME"]
    tile_set_filepath = f"{base_path}/{tile_set_name}"
    return f"{tile_set_filepath}/{tile_set_name}.json"


class Solver:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('../settings.ini')

        self.grid = Grid(get_json_path(config),
                         int(config['grid']['GRID_DIM_WIDTH']),
                         int(config['grid']['GRID_DIM_HEIGHT']))
        self.fail_condition = config['contradiction']['FAIL_CONDITION']

    def solve_next(self):
        # If there remains a single tile not collapsed...
        if not self.grid.finished_collapsing:
            collapsed, x, y = self.grid.collapse_next_tile()
            if not collapsed:
                print(f"Cannot complete this pattern...")
                print(f"FAIL_CONDITION set to {self.fail_condition}")
                if self.fail_condition == "END":
                    print(f"Ending collapse")
                    return False
                #elif FAIL_CONDITION == "RESET":
                #    print(f"Resetting collapse")
                #    setup()
                # elif FAIL_CONDITION == "RESET_FROM_FAIL":
                #    print(f"Resetting collapse from failure cell [{x},{y}]")
                #    setup()
                #    grid[x][y].collapse() #doesn't seem to cause the chain reaction i'd expect
        return True


    #get/set
    def is_solved(self):
        return self.grid.finished_collapsing

    def get_grid(self):
        return self.grid.grid

if __name__ == "__main__":
    solver = Solver()
    while not solver.is_solved():
        solver.solve_next()
        solver.get_grid()
    for row in solver.grid.grid:
        for node in row:
            print(node)