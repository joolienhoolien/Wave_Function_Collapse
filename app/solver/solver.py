from app.solver.grid import Grid
import configparser


def get_json_path(config):
    """Parse the settings.ini file to find the path to the tileset instructions"""
    base_path = f"../../{config['tiles']['TILE_SET_FOLDER']}"
    tile_set_name = config["tiles"]["TILE_SET_NAME"]
    tile_set_filepath = f"{base_path}/{tile_set_name}"
    return f"{tile_set_filepath}/{tile_set_name}.json"


class Solver:
    """
    Main class in wave function collapse backend. Responsible for orchestrating the collapse.
    If this class is ran as the main executable, rather than using a GUI to call this class, it prints to the command line.
    """
    def __init__(self, debug=False):
        """
        Creates a solver instance given a settings.ini, set of tiles, and tile instructions are in the directory.
            grid: Reference to the grid object holding the node data
            fail_condition: determines how the application logic behaves when a contradictory collapse is generated
        """
        config = configparser.ConfigParser()
        config.read('../../settings.ini')
        if debug: print("Creating solver...")

        self.grid = Grid(get_json_path(config),
                         int(config['grid']['GRID_DIM_WIDTH']),
                         int(config['grid']['GRID_DIM_HEIGHT']),
                         (config['tiles']['DIRECTIONS']).split(','),
                         debug=debug)
        self.fail_condition = config['contradiction']['FAIL_CONDITION']
        self.debug=debug

    def solve_next(self):
        """
        Solve the next step of the collapse.
        Return:
            False if the collapse contradicted
            True if the collapse was successful.
        """
        # If there remains a single tile not collapsed...
        if not self.grid.finished_collapsing:
            collapsed = self.grid.collapse_next_tile()
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
        """Returns whether the solver has finished collapsing the grid."""
        return self.grid.finished_collapsing

    def get_grid(self):
        """Return the 2d grid of nodes - NOT the grid object."""
        return self.grid.grid

if __name__ == "__main__":
    solver = Solver()
    while not solver.is_solved():
        solver.solve_next()
        solver.get_grid()
    for row in solver.grid.grid:
        for node in row:
            print(node)