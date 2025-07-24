"""
#Algorithm steps:
1. Create tiles
    1a. Set up tile prototypes
        - Read from a JSON file
        - Create Tile objects
            Tile's have an **image path**
    1b. Set up tile permutations
        - Make a new tile using a prototype
            - Rotate tiles based on a json field
            - images, and sides
    1c. Set up tile neighbors
        - For each tile, look at each other tile and compare sockets in opposite directions
            - If the sockets match, they can be neighbors
2. Create a 2d grid of nodes
    2a. For each grid[i][j] (based on settings dimensions)...
        - Create a node which holds:
            - the **possibility space** (aka which tiles can it be?)
            - [i][j] for when we need to look at it's neighbors.
                - At the start, every node on the grid can be every tile.
current state: we have a set of Tiles, and a grid of full possibilities. Nothing is rendered to the screen.
We probably want to return this information to the caller - which is likely a frontend.
Ex: It says "Please set me up for this tile set"
    ... maybe we want to be able to start via a button that says "start". Or we want to display the different tile options
    ... or we want to let them set constraints. This is when it would happen. Or weights!
3. Adjust anything in the front end. For now this step will be glossed over.
    One detail is that when this step is over, the front end should be rendering the initial state.
4. Solver.solve() the puzzle / collapse the wave
    Render the starting image, maybe handled in step 3
    While the puzzle is solvable and unsolved:
        4a. Collapse a random node from the set of lowest entropy nodes (at the start this is the full set of nodes)
            If there is a node with 0 options, and collapsed=False, the is not solvable. Exit this loop and return failure
            4a.i. When a node is told to be collapsed...
                Collapse the tile
                    - Set it to collapsed=True
                    - Set it's image
                    - Set it's options to set()
        4b. Propagate:
            Add it's neighbors to the stack
                While stack:
                    currNode = stack.pop
                    if not collapsed:
                        temp_options = options
                        Calculate options
                            #Look up,down,left,right and set options = intersection(options, union(other_node.options[opposite_direction]))
                                ex: node_up = [currNode.x][currNode.y - 1]
                                currNode.options = currNode.options & union(node_up.options[down])
                                #Maybe have a function for calculating possible neighbors at the node level?
                        if temp_options == currNode.options,
                            return
                        else:
                            add neighbors to stack
        4c. Render the current image / return information to front end to render
5. Stop solving and return control to the front end. Maybe we can save the image or run again or something
"""
import json
import sys

from pygame.locals import *
import random
from tile import Tile, copy_tile_and_rotate
from cell import Cell
from settings import *

FINISHED_COLLAPSING = False
TILES = []
grid = []

#Base tile's keys describe number of rotations to perform on the tile
BASE_TILES = {
    4: [],
    2: [],
    0: []
}

def setup_tiles_from_json(filepath=TILE_SET_FILEPATH):
    try:
        with open(filepath, 'r') as file:
            data = json.load(file)
        for tile in data['tile_set']:
            sides = {i+1:value for i,(side,value) in enumerate(tile['sides'].items())}
            BASE_TILES[tile['number_of_rotations']].append(Tile(tile['image_path'],sides))
    except FileNotFoundError as error:
        print(error)
        raise

def setup_tiles_set1():
    BASE_TILES[0].append(Tile("../tile_sets/set1/blank.png",
                      {UP: "0", RIGHT: "0", DOWN: "0", LEFT: "0"}))
    BASE_TILES[4].append(Tile("../tile_sets/set1/T.png",
                           {UP: "1", RIGHT: "1", DOWN: "0", LEFT: "1"}))

def setup_tiles_pcb():
    """
    color definitions:
        GREY: 0
        GREEN: 1
        L GREEN: 2
        L GREY: 3
    :return:
    """
    BASE_TILES[0].append(Tile("../tile_sets/pcb/0.png",
                      {UP: "000", RIGHT: "000", DOWN: "000", LEFT: "000"}))
    BASE_TILES[0].append(Tile("../tile_sets/pcb/1.png",
                      {UP: "111", RIGHT: "111", DOWN: "111", LEFT: "111"}))
    BASE_TILES[4].append(Tile("../tile_sets/pcb/2.png",
                           {UP: "111", RIGHT: "121", DOWN: "111", LEFT: "111"}))
    BASE_TILES[2].append(Tile("../tile_sets/pcb/3.png",
                           {UP: "111", RIGHT: "131", DOWN: "111", LEFT: "131"}))
    BASE_TILES[4].append(Tile("../tile_sets/pcb/4.png",
                           {UP: "011", RIGHT: "121", DOWN: "110", LEFT: "000"}))
    BASE_TILES[4].append(Tile("../tile_sets/pcb/5.png",
                           {UP: "011", RIGHT: "111", DOWN: "111", LEFT: "110"}))
    BASE_TILES[2].append(Tile("../tile_sets/pcb/6.png",
                           {UP: "111", RIGHT: "121", DOWN: "111", LEFT: "121"}))
    BASE_TILES[2].append(Tile("../tile_sets/pcb/7.png",
                           {UP: "131", RIGHT: "121", DOWN: "131", LEFT: "121"}))
    BASE_TILES[4].append(Tile("../tile_sets/pcb/8.png",
                           {UP: "131", RIGHT: "111", DOWN: "121", LEFT: "111"}))
    BASE_TILES[4].append(Tile("../tile_sets/pcb/9.png",
                           {UP: "121", RIGHT: "121", DOWN: "111", LEFT: "121"}))
    BASE_TILES[2].append(Tile("../tile_sets/pcb/10.png",
                           {UP: "121", RIGHT: "121", DOWN: "121", LEFT: "121"}))
    BASE_TILES[4].append(Tile("../tile_sets/pcb/11.png",
                           {UP: "121", RIGHT: "121", DOWN: "111", LEFT: "111"}))
    BASE_TILES[2].append(Tile("../tile_sets/pcb/12.png",
                           {UP: "111", RIGHT: "121", DOWN: "111", LEFT: "121"}))

def setup_tiles_circles(black_weight = 1, white_weight = 1):
    """
    color definitions:
        black: 0
        white: 1
    :return:
    """
    for _ in range(black_weight):
        BASE_TILES[0].append(Tile("../tile_sets/circles/b.png",
                          {UP: "0", RIGHT: "0", DOWN: "0", LEFT: "0"}))
    BASE_TILES[4].append(Tile("../tile_sets/circles/b_half.png",
                      {UP: "0", RIGHT: "1", DOWN: "1", LEFT: "1"}))
    BASE_TILES[2].append(Tile("../tile_sets/circles/b_i.png",
                      {UP: "0", RIGHT: "1", DOWN: "0", LEFT: "1"}))
    BASE_TILES[4].append(Tile("../tile_sets/circles/b_quarter.png",
                  {UP: "0", RIGHT: "0", DOWN: "1", LEFT: "1"}))

    for _ in range(white_weight):
        BASE_TILES[0].append(Tile("../tile_sets/circles/w.png",
                          {UP: "1", RIGHT: "1", DOWN: "1", LEFT: "1"}))
    BASE_TILES[4].append(Tile("../tile_sets/circles/w_half.png",
                      {UP: "1", RIGHT: "0", DOWN: "0", LEFT: "0"}))
    BASE_TILES[2].append(Tile("../tile_sets/circles/w_i.png",
                      {UP: "1", RIGHT: "0", DOWN: "1", LEFT: "0"}))
    BASE_TILES[4].append(Tile("../tile_sets/circles/w_quarter.png",
                      {UP: "1", RIGHT: "1", DOWN: "0", LEFT: "0"}))

def setup_tiles_sproutlands_grass(land_weight=1, water_weight=10):
    """
    color definitions:
        0: water
        1: land
    :return:
    """
    for _ in range(land_weight): pass
    BASE_TILES[0].append(Tile("../tile_sets/sprout lands/grass_tiles_v2/slices/tiles__1.png",
                                  {UP: "000", RIGHT: "011", DOWN: "110", LEFT: "000"}))
    BASE_TILES[0].append(Tile("../tile_sets/sprout lands/grass_tiles_v2/slices/tiles__2.png",
                                  {UP: "000", RIGHT: "011", DOWN: "111", LEFT: "110"}))
    BASE_TILES[0].append(Tile("../tile_sets/sprout lands/grass_tiles_v2/slices/tiles__3.png",
                                  {UP: "000", RIGHT: "000", DOWN: "011", LEFT: "110"}))
    BASE_TILES[0].append(Tile("../tile_sets/sprout lands/grass_tiles_v2/slices/tiles__4.png",
                                  {UP: "000", RIGHT: "000", DOWN: "010", LEFT: "000"}))
    BASE_TILES[0].append(Tile("../tile_sets/sprout lands/grass_tiles_v2/slices/tiles__5.png",
                                  {UP: "000", RIGHT: "010", DOWN: "010", LEFT: "000"}))
    BASE_TILES[0].append(Tile("../tile_sets/sprout lands/grass_tiles_v2/slices/tiles__6.png",
                                  {UP: "000", RIGHT: "010", DOWN: "011", LEFT: "110"}))
    BASE_TILES[0].append(Tile("../tile_sets/sprout lands/grass_tiles_v2/slices/tiles__7.png",
                                  {UP: "000", RIGHT: "011", DOWN: "110", LEFT: "010"}))
    BASE_TILES[0].append(Tile("../tile_sets/sprout lands/grass_tiles_v2/slices/tiles__8.png",
                                  {UP: "000", RIGHT: "000", DOWN: "010", LEFT: "010"}))
    BASE_TILES[0].append(Tile("../tile_sets/sprout lands/grass_tiles_v2/slices/tiles__9.png",
                                  {UP: "000", RIGHT: "010", DOWN: "010", LEFT: "010"}))
    BASE_TILES[0].append(Tile("../tile_sets/sprout lands/grass_tiles_v2/slices/tiles__10.png",
                                  {UP: "110", RIGHT: "011", DOWN: "110", LEFT: "011"}))
    BASE_TILES[0].append(Tile("../tile_sets/sprout lands/grass_tiles_v2/slices/tiles__12.png",
                                  {UP: "011", RIGHT: "111", DOWN: "110", LEFT: "000"}))
    BASE_TILES[0].append(Tile("../tile_sets/sprout lands/grass_tiles_v2/slices/tiles__13.png",
                                  {UP: "111", RIGHT: "111", DOWN: "111", LEFT: "111"}))
    BASE_TILES[0].append(Tile("../tile_sets/sprout lands/grass_tiles_v2/slices/tiles__14.png",
                                  {UP: "110", RIGHT: "000", DOWN: "011", LEFT: "111"}))
    BASE_TILES[0].append(Tile("../tile_sets/sprout lands/grass_tiles_v2/slices/tiles__15.png",
                                  {UP: "010", RIGHT: "000", DOWN: "010", LEFT: "000"}))
    BASE_TILES[0].append(Tile("../tile_sets/sprout lands/grass_tiles_v2/slices/tiles__16.png",
                                  {UP: "011", RIGHT: "110", DOWN: "010", LEFT: "000"}))
    BASE_TILES[0].append(Tile("../tile_sets/sprout lands/grass_tiles_v2/slices/tiles__17.png",
                                  {UP: "111", RIGHT: "110", DOWN: "011", LEFT: "111"}))
    BASE_TILES[0].append(Tile("../tile_sets/sprout lands/grass_tiles_v2/slices/tiles__18.png",
                                  {UP: "111", RIGHT: "111", DOWN: "110", LEFT: "011"}))
    BASE_TILES[0].append(Tile("../tile_sets/sprout lands/grass_tiles_v2/slices/tiles__19.png",
                                  {UP: "110", RIGHT: "000", DOWN: "010", LEFT: "011"}))
    BASE_TILES[0].append(Tile("../tile_sets/sprout lands/grass_tiles_v2/slices/tiles__20.png",
                                  {UP: "111", RIGHT: "110", DOWN: "010", LEFT: "011"}))
    BASE_TILES[0].append(Tile("../tile_sets/sprout lands/grass_tiles_v2/slices/tiles__21.png",
                                  {UP: "011", RIGHT: "110", DOWN: "011", LEFT: "110"}))
    BASE_TILES[0].append(Tile("../tile_sets/sprout lands/grass_tiles_v2/slices/tiles__23.png",
                                  {UP: "011", RIGHT: "110", DOWN: "000", LEFT: "000"}))
    BASE_TILES[0].append(Tile("../tile_sets/sprout lands/grass_tiles_v2/slices/tiles__24.png",
                                  {UP: "111", RIGHT: "110", DOWN: "000", LEFT: "011"}))
    BASE_TILES[0].append(Tile("../tile_sets/sprout lands/grass_tiles_v2/slices/tiles__25.png",
                                  {UP: "110", RIGHT: "000", DOWN: "000", LEFT: "011"}))
    BASE_TILES[0].append(Tile("../tile_sets/sprout lands/grass_tiles_v2/slices/tiles__26.png",
                                  {UP: "010", RIGHT: "000", DOWN: "000", LEFT: "000"}))
    BASE_TILES[0].append(Tile("../tile_sets/sprout lands/grass_tiles_v2/slices/tiles__27.png",
                                  {UP: "010", RIGHT: "011", DOWN: "110", LEFT: "000"}))
    BASE_TILES[0].append(Tile("../tile_sets/sprout lands/grass_tiles_v2/slices/tiles__28.png",
                                  {UP: "110", RIGHT: "011", DOWN: "111", LEFT: "111"}))
    BASE_TILES[0].append(Tile("../tile_sets/sprout lands/grass_tiles_v2/slices/tiles__29.png",
                                  {UP: "011", RIGHT: "111", DOWN: "111", LEFT: "110"}))
    BASE_TILES[0].append(Tile("../tile_sets/sprout lands/grass_tiles_v2/slices/tiles__30.png",
                                  {UP: "010", RIGHT: "000", DOWN: "011", LEFT: "110"}))
    BASE_TILES[0].append(Tile("../tile_sets/sprout lands/grass_tiles_v2/slices/tiles__31.png",
                                  {UP: "010", RIGHT: "011", DOWN: "111", LEFT: "110"}))
    BASE_TILES[0].append(Tile("../tile_sets/sprout lands/grass_tiles_v2/slices/tiles__32.png",
                                  {UP: "010", RIGHT: "011", DOWN: "110", LEFT: "010"}))
    BASE_TILES[0].append(Tile("../tile_sets/sprout lands/grass_tiles_v2/slices/tiles__33.png",
                                  {UP: "010", RIGHT: "010", DOWN: "011", LEFT: "110"}))
    BASE_TILES[0].append(Tile("../tile_sets/sprout lands/grass_tiles_v2/slices/tiles__34.png",
                                  {UP: "000", RIGHT: "010", DOWN: "000", LEFT: "000"}))
    BASE_TILES[0].append(Tile("../tile_sets/sprout lands/grass_tiles_v2/slices/tiles__35.png",
                                  {UP: "000", RIGHT: "010", DOWN: "000", LEFT: "010"}))
    BASE_TILES[0].append(Tile("../tile_sets/sprout lands/grass_tiles_v2/slices/tiles__36.png",
                                  {UP: "000", RIGHT: "000", DOWN: "000", LEFT: "010"}))
    BASE_TILES[0].append(Tile("../tile_sets/sprout lands/grass_tiles_v2/slices/tiles__37.png",
                                  {UP: "000", RIGHT: "000", DOWN: "000", LEFT: "000"}))
    BASE_TILES[0].append(Tile("../tile_sets/sprout lands/grass_tiles_v2/slices/tiles__38.png",
                                  {UP: "010", RIGHT: "010", DOWN: "000", LEFT: "000"}))
    BASE_TILES[0].append(Tile("../tile_sets/sprout lands/grass_tiles_v2/slices/tiles__39.png",
                                  {UP: "110", RIGHT: "010", DOWN: "000", LEFT: "100"}))
    BASE_TILES[0].append(Tile("../tile_sets/sprout lands/grass_tiles_v2/slices/tiles__40.png",
                                  {UP: "011", RIGHT: "110", DOWN: "000", LEFT: "010"}))
    BASE_TILES[0].append(Tile("../tile_sets/sprout lands/grass_tiles_v2/slices/tiles__41.png",
                                  {UP: "010", RIGHT: "000", DOWN: "000", LEFT: "010"}))
    BASE_TILES[0].append(Tile("../tile_sets/sprout lands/grass_tiles_v2/slices/tiles__42.png",
                                  {UP: "010", RIGHT: "010", DOWN: "000", LEFT: "010"}))
    BASE_TILES[0].append(Tile("../tile_sets/sprout lands/grass_tiles_v2/slices/tiles__43.png",
                                  {UP: "011", RIGHT: "110", DOWN: "010", LEFT: "010"}))
    BASE_TILES[0].append(Tile("../tile_sets/sprout lands/grass_tiles_v2/slices/tiles__44.png",
                                  {UP: "110", RIGHT: "010", DOWN: "010", LEFT: "011"}))
    BASE_TILES[0].append(Tile("../tile_sets/sprout lands/grass_tiles_v2/slices/tiles__49.png",
                                  {UP: "010", RIGHT: "010", DOWN: "010", LEFT: "000"}))
    BASE_TILES[0].append(Tile("../tile_sets/sprout lands/grass_tiles_v2/slices/tiles__50.png",
                                  {UP: "110", RIGHT: "010", DOWN: "011", LEFT: "111"}))
    BASE_TILES[0].append(Tile("../tile_sets/sprout lands/grass_tiles_v2/slices/tiles__51.png",
                                  {UP: "011", RIGHT: "111", DOWN: "110", LEFT: "010"}))
    BASE_TILES[0].append(Tile("../tile_sets/sprout lands/grass_tiles_v2/slices/tiles__52.png",
                                  {UP: "010", RIGHT: "000", DOWN: "010", LEFT: "010"}))
    BASE_TILES[0].append(Tile("../tile_sets/sprout lands/grass_tiles_v2/slices/tiles__53.png",
                                  {UP: "010", RIGHT: "010", DOWN: "010", LEFT: "010"}))
    BASE_TILES[0].append(Tile("../tile_sets/sprout lands/grass_tiles_v2/slices/tiles__56.png",
                                  {UP: "111", RIGHT: "111", DOWN: "111", LEFT: "111"}))
    BASE_TILES[0].append(Tile("../tile_sets/sprout lands/grass_tiles_v2/slices/tiles__57.png",
                                  {UP: "111", RIGHT: "111", DOWN: "111", LEFT: "111"}))
    BASE_TILES[0].append(Tile("../tile_sets/sprout lands/grass_tiles_v2/slices/tiles__58.png",
                                  {UP: "111", RIGHT: "111", DOWN: "111", LEFT: "111"}))
    BASE_TILES[0].append(Tile("../tile_sets/sprout lands/grass_tiles_v2/slices/tiles__59.png",
                                  {UP: "111", RIGHT: "111", DOWN: "111", LEFT: "111"}))
    BASE_TILES[0].append(Tile("../tile_sets/sprout lands/grass_tiles_v2/slices/tiles__60.png",
                                  {UP: "111", RIGHT: "111", DOWN: "111", LEFT: "111"}))
    BASE_TILES[0].append(Tile("../tile_sets/sprout lands/grass_tiles_v2/slices/tiles__61.png",
                                  {UP: "111", RIGHT: "111", DOWN: "111", LEFT: "111"}))
    BASE_TILES[0].append(Tile("../tile_sets/sprout lands/grass_tiles_v2/slices/tiles__67.png",
                                  {UP: "111", RIGHT: "111", DOWN: "111", LEFT: "111"}))
    BASE_TILES[0].append(Tile("../tile_sets/sprout lands/grass_tiles_v2/slices/tiles__68.png",
                                  {UP: "111", RIGHT: "111", DOWN: "111", LEFT: "111"}))
    BASE_TILES[0].append(Tile("../tile_sets/sprout lands/grass_tiles_v2/slices/tiles__69.png",
                                  {UP: "111", RIGHT: "111", DOWN: "111", LEFT: "111"}))
    BASE_TILES[0].append(Tile("../tile_sets/sprout lands/grass_tiles_v2/slices/tiles__70.png",
                                  {UP: "111", RIGHT: "111", DOWN: "111", LEFT: "111"}))
    BASE_TILES[0].append(Tile("../tile_sets/sprout lands/grass_tiles_v2/slices/tiles__71.png",
                                  {UP: "111", RIGHT: "111", DOWN: "111", LEFT: "111"}))
    BASE_TILES[0].append(Tile("../tile_sets/sprout lands/grass_tiles_v2/slices/tiles__72.png",
                                  {UP: "111", RIGHT: "111", DOWN: "111", LEFT: "111"}))
    for _ in range(water_weight):
        BASE_TILES[0].append(Tile("../tile_sets/sprout lands/grass_tiles_v2/slices/tiles__77.png",
                                      {UP: "000", RIGHT: "000", DOWN: "000", LEFT: "000"}))

def setup_tiles(filepath=None, tile_set=None):
    if filepath:
        setup_tiles_from_json(filepath)
    elif tile_set:
        if tile_set == "set1":
            setup_tiles_set1()
        elif tile_set == "pcb":
            setup_tiles_pcb()
        elif tile_set == "circles":
            setup_tiles_circles(TILE_WEIGHTS["black"], TILE_WEIGHTS["white"])
        elif tile_set == "sproutlands_grass":
            setup_tiles_sproutlands_grass()
    for num_rotations in BASE_TILES:
        for tile in BASE_TILES[num_rotations]:
            if num_rotations == 0:
                TILES.append(tile)
            else:
                for i in range(num_rotations):
                    rotated_tile = copy_tile_and_rotate(tile, i)
                    TILES.append(rotated_tile)

def setup():
    global FINISHED_COLLAPSING
    FINISHED_COLLAPSING = False
    #setup_tiles(tile_set=TILE_SET)
    setup_tiles(filepath=TILE_SET_FILEPATH)

    #Set up neighbors for tiles
    for tile in TILES:
        tile.set_valid_neighbors(TILES)

    #Set up grid of cells
    global grid
    grid = [[0 for _ in range(GRID_DIM_HEIGHT)] for _ in range(GRID_DIM_WIDTH)]
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            grid[i][j] = Cell(i, j, TILES)

def draw_tiles():
    if DEBUG: print("drawing\n")
    count = 0
    for row in grid:
        for cell in row:
            cell.draw(DISPLAYSURF)
            count += 1
    if DEBUG: print(f"drew {count} cells!~~~\n")

def collapse_tiles():
    global FINISHED_COLLAPSING

    # 1. Obtain a list of tiles coordinates such that they have the least amount of options
    lowest_entropy = len(TILES)
    lowest_entropy_cells = []
    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            #TODO: Set this up so that we do not need to even look at this tile
            #Perhaps grid is a list of objects with x,y coord
                #or dictionary but i dont think that will work
            #... and when we collapse something, we remove it from the array
            if cell.is_collapsed() or len(cell.options) > lowest_entropy:
                continue
            elif len(cell.options) == lowest_entropy:
                lowest_entropy_cells.append((cell, i, j))
            else:
                lowest_entropy = len(cell.options)
                lowest_entropy_cells = [(cell, i, j)]
    if lowest_entropy_cells:

        # 2. From this list, randomly choose a tile to collapse
        to_collapse_data = random.choice(lowest_entropy_cells)
        cell, x, y = to_collapse_data
        if not cell.collapse():
            print(f"found contradiction in cell ({x},{y})")
            FINISHED_COLLAPSING = True
            return False, x, y

        # 3. Update neighboring tiles using intersection of rules and options
        try:
            cell_left = grid[(x - 1) % GRID_DIM_WIDTH][y]
            if not cell_left.is_collapsed():
                cell_left.update_options(cell_left.options & cell.tile.valid_neighbors[RIGHT])
            cell_right = grid[(x + 1) % GRID_DIM_WIDTH][y]
            if not cell_right.is_collapsed():
                cell_right.update_options(cell_right.options & cell.tile.valid_neighbors[LEFT])
            cell_up = grid[x][(y - 1) % GRID_DIM_HEIGHT]
            if not cell_up.is_collapsed():
                cell_up.update_options(cell_up.options & cell.tile.valid_neighbors[DOWN])
            cell_down = grid[x][(y + 1) % GRID_DIM_HEIGHT]
            if not cell_down.is_collapsed():
                cell_down.update_options(cell_down.options & cell.tile.valid_neighbors[UP])
        except AttributeError:
            print(f"found contradiction in cell ({x},{y})")
            FINISHED_COLLAPSING = True
            return False, x, y

    else:
        FINISHED_COLLAPSING = True
    return True, None, None

def game_loop():
    global FINISHED_COLLAPSING
    while True:
        #Allow exiting of program with X button
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        #If there remains a single tile not collapsed...
        if not FINISHED_COLLAPSING:
            collapsed, cell_x, cell_y = collapse_tiles()
            if not collapsed:
                print(f"Cannot complete this pattern...")
                print(f"FAIL_CONDITION set to {FAIL_CONDITION}")
                if FAIL_CONDITION == "END":
                    print(f"Ending collapse")
                elif FAIL_CONDITION == "RESET":
                    print(f"Resetting collapse")
                    setup()
                #elif FAIL_CONDITION == "RESET_FROM_FAIL":
                #    print(f"Resetting collapse from failure cell [{cell_x},{cell_y}]")
                #    setup()
                #    grid[cell_x][cell_y].collapse() #doesn't seem to cause the chain reaction i'd expect

        draw_tiles()
        pygame.display.update()
        FramePerSec.tick(FPS)

def get_cell_info():
    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            #print(f"[{i}][{j}] | entropy:{len(cell.options)} | tile: {cell.tile.image_path} | options: {[tile.image_path for tile in cell.options]}")
            print(f"[{i}][{j}] | coordinates:  ")

if __name__ == "__main__":
    pygame.init()
    setup()
    game_loop()
