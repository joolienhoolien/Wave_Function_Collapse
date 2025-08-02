# 2D Wave Function Collapse Visualizer
Generates an image using a 2D grid of tiles. Utilizes the wave function collapse 
algorithm in two dimensions. The image is generated "randomly" and will be novel and unique.

Here are some examples:
#### Circles tile set, no constraints, default tile weights
![circles_aug_2.gif](output/gifs/circles_aug_2.gif)
#### Grass Tiles tile set, no constraints, heavily weighted for landlocked or water tiles
![sprout_lands_1.gif](output/gifs/sprout_lands_1.gif)
# Installation
Simply clone the repository and install the requirements listed below in `technologies used and requirements`.

### Technologies Used and Requirements
This project uses mostly core python, except for `PyGame` which
is used for the frontend display. 
Pygame can be installed via `pip install pygame`

# Basic Usage
To use it without any modifications, simply run `pygame_frontend.py` or `solver.py`.
- `pygame_frontend.py` is the implementation of the visualizer and the intended way to run the program.
- `solver.py` runs without updating any images and only generates CLI information about the grid. This is the "backend class"
If you want to change any settings (tile set, constraints, weights, etc) see the below section `Advanced Usage`

# Tilesets
The package comes with a few tilesets. They are found in `base_tiles`.
Within each set contains the images and a `JSON` file containing a set of rules.
The program parses the `JSON` and expects the images referenced within the rules to be
in the same folder. 
#### Tile Attributes
- id: unique identifier
- sides: the rules details in `tile rules` for each side
- weight: how frequently this tile will be chosen compared to other tiles.
  - if weight is not declared on a tile, it defaults to 1
- image_path: the file name, assumed to be within the same folder as this `JSON` file
- number_of_rotations: number representing the number of different tiles to create from this tile. 
  - use any non-negative integer, but it will only rotate 0, 1, 2, 3 times and at most create 4 unique permutations.

### Tile Rules
To set up the rules for a tile, we utilize a socket system wherein each side of a
tile is represented by a string. Two tiles can be next to each other if their corresponding
sides' strings are *reverse of each other.*
- Example: 
  - Tile A's "up" side has a socket "1234a"
  - Tile B's "down" side has a socket "bdf"
  - Tile C's "down" side has a socket "a4321"
  - We place Tile A on the board. We check to see if Tile B can go above Tile A and so
compare Tile A's "up" and tile B's "down". However "1234a" != "fdb" (reverse of Tile B) so they cannot be neighbors.
  - We now check if Tile C can go above Tile A, and indeed "1234a" == "1234a" (reverse of Tile C)


## Constraints

## Failures / Contradictions


# Advanced Usage
### Changing the tileset
Go to the `settings.ini` file in the root directory and change `TILE_SET_NAME` to one of the folder names
in "base_tiles". 

### Changing a tileset rule
Within `base_tiles/{the set you are using}`, open the `JSON` ruleset. 
Each object in the `tile_set` section represents a tile. 

### Creating your own tileset
If you wish to create your own tileset, you must do the following:
- Create a new folder under base_tiles with the name of your set.
  - This folder must include `png` images and a `json` with the tile rules. Use one of the 
other tilesets as a guideline and reference "tile rules" for creating socket rules
- Change the `TILE_SET_NAME` field in `settings.ini` to the tileset name you chose.

It is a good idea to draw out your tileset when creating your sockets so as not to make mistakes
when outlining it in the JSON file.
