"""
Responsible for:
    - Settings (grid dimensions, fail condition, tile_set)
    - Creating and managing the grid
"""
from grid import Grid
from settings import *

class Solver:
    def __init__(self):
        #TODO: read settings from solver_settings.json
        tile_set_filepath = TILE_SET_FILEPATH
        self.grid = Grid(tile_set_filepath, GRID_DIM_WIDTH, GRID_DIM_HEIGHT)

    def solve_next(self):
        # If there remains a single tile not collapsed...
        if not self.grid.finished_collapsing:
            collapsed, x, y = self.grid.collapse_next_tile()
            if not collapsed:
                print(f"Cannot complete this pattern...")
                print(f"FAIL_CONDITION set to {FAIL_CONDITION}")
                if FAIL_CONDITION == "END":
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
