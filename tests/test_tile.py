import configparser
import pytest
from app.solver.tile import Tile


@pytest.fixture
def setup_tile_blank():
    sides = {
        "up": "0",
        "right": "0",
        "down": "0",
        "left": "0"
    }
    image_path = "blank.png"
    rotations = 0
    full_image_path = False
    config = configparser.ConfigParser()
    config.read('../settings.ini')
    tile = Tile(image_path, sides, rotations, full_image_path, config)
    yield tile

def test_blank_tile_init(setup_tile_blank):
    assert setup_tile_blank is not None
    assert setup_tile_blank.image_path == "../../base_tiles/tests/blank.png"
    assert setup_tile_blank.sides == {
        "up": "0",
        "right": "0",
        "down": "0",
        "left": "0"
    }
    assert setup_tile_blank.rotations == 0
    assert setup_tile_blank.valid_neighbors == {
        'down': set(),
        'left': set(),
        'right': set(),
        'up': set()
    }
    assert setup_tile_blank.directions == ['up','right','down','left']


@pytest.fixture
def setup_tile_symmetric():
    sides = {
        "up": "1",
        "right": "1",
        "down": "0",
        "left": "1"
    }
    image_path = "T.png"
    rotations = 4
    full_image_path = False
    config = configparser.ConfigParser()
    config.read('../settings.ini')
    tile  = Tile(image_path, sides, rotations, full_image_path, config)
    yield tile

def test_symmetric_tile_init(setup_tile_symmetric):
    assert setup_tile_symmetric is not None
    assert setup_tile_symmetric.image_path == "../../base_tiles/tests/T.png"
    assert setup_tile_symmetric.sides == {
        "up": "1",
        "right": "1",
        "down": "0",
        "left": "1"
    }
    assert setup_tile_symmetric.rotations == 4
    assert setup_tile_symmetric.valid_neighbors == {
        'down': set(),
        'left': set(),
        'right': set(),
        'up': set()
    }
    assert setup_tile_symmetric.directions == ['up', 'right', 'down', 'left']


@pytest.fixture
def setup_tile_asymmetric():
    sides = {"up": "011", "right": "111", "down": "111", "left": "110"}
    image_path = "5.png"
    rotations = 4
    full_image_path = False
    config = configparser.ConfigParser()
    config.read('../settings.ini')
    tile = Tile(image_path, sides, rotations, full_image_path, config)
    yield tile

def test_asymmetric_tile_init(setup_tile_asymmetric):
    assert setup_tile_asymmetric is not None
    assert setup_tile_asymmetric.image_path == "../../base_tiles/tests/5.png"
    assert setup_tile_asymmetric.sides == {"up": "011", "right": "111", "down": "111", "left": "110"}
    assert setup_tile_asymmetric.rotations == 4
    assert setup_tile_asymmetric.valid_neighbors == {
        'down': set(),
        'left': set(),
        'right': set(),
        'up': set()
    }
    assert setup_tile_asymmetric.directions == ['up', 'right', 'down', 'left']


@pytest.fixture
def setup_tile_asymmetric_2():
    sides = {"up": "011", "right": "121", "down": "110", "left": "000"}
    image_path = "4.png"
    rotations = 4
    full_image_path = False
    config = configparser.ConfigParser()
    config.read('../settings.ini')
    tile = Tile(image_path, sides, rotations, full_image_path, config)
    yield tile

def test_asymmetric_2_tile_init(setup_tile_asymmetric_2):
    assert setup_tile_asymmetric_2 is not None
    assert setup_tile_asymmetric_2.image_path == "../../base_tiles/tests/4.png"
    assert setup_tile_asymmetric_2.sides == {"up": "011", "right": "121", "down": "110", "left": "000"}
    assert setup_tile_asymmetric_2.rotations == 4
    assert setup_tile_asymmetric_2.valid_neighbors == {
        'down': set(),
        'left': set(),
        'right': set(),
        'up': set()
    }
    assert setup_tile_asymmetric_2.directions == ['up', 'right', 'down', 'left']


@pytest.fixture
def setup_tile_2rotations():
    sides={"up": "0", "right": "1", "down": "0", "left": "1"}
    image_path = "b_i.png"
    rotations = 2
    full_image_path = False
    config = configparser.ConfigParser()
    config.read('../settings.ini')
    tile = Tile(image_path, sides, rotations, full_image_path, config)
    yield tile

def test_2rotations_tile_init(setup_tile_2rotations):
    assert setup_tile_2rotations is not None
    assert setup_tile_2rotations.image_path == "../../base_tiles/tests/b_i.png"
    assert setup_tile_2rotations.sides == {"up": "0", "right": "1", "down": "0", "left": "1"}
    assert setup_tile_2rotations.rotations == 2
    assert setup_tile_2rotations.valid_neighbors == {
        'down': set(),
        'left': set(),
        'right': set(),
        'up': set()
    }
    assert setup_tile_2rotations.directions == ['up', 'right', 'down', 'left']

@pytest.fixture
def setup_valid_neighbors(setup_tile_blank, setup_tile_symmetric,
                         setup_tile_asymmetric,setup_tile_asymmetric_2,setup_tile_2rotations):
    base_tiles = [setup_tile_blank, setup_tile_symmetric,
                         setup_tile_asymmetric,setup_tile_asymmetric_2,setup_tile_2rotations]
    yield base_tiles



def test_valid_neighbors_no_permutes(setup_valid_neighbors):
    for tile in setup_valid_neighbors:
        tile.set_valid_neighbors(setup_valid_neighbors)
    for tile in setup_valid_neighbors:
        assert tile.valid_neighbors is not None
    assert len(setup_valid_neighbors[0].valid_neighbors['up']) == 3
    assert len(setup_valid_neighbors[0].valid_neighbors['down']) == 2
    assert len(setup_valid_neighbors[1].valid_neighbors['left']) == 2
    assert len(setup_valid_neighbors[1].valid_neighbors['down']) == 2
    assert len(setup_valid_neighbors[1].valid_neighbors['down']) == 2
    assert len(setup_valid_neighbors[4].valid_neighbors['up']) == 3
    assert len(setup_valid_neighbors[2].valid_neighbors['up']) == 1
    assert len(setup_valid_neighbors[2].valid_neighbors['left']) == 0
    assert len(setup_valid_neighbors[3].valid_neighbors['up']) == 1

def test_valid_neighbors_with_permutes(setup_valid_neighbors):
    permuted_tiles = []
    for tile in setup_valid_neighbors:
        if tile.rotations == 0:
            permuted_tiles.append(tile)
        else:
            for rotation in range(tile.rotations):
                permuted_tiles.append(tile.copy_tile_and_rotate(rotation))

    blank, t, circle1, pcb1, pcb2 = None, None, None, None, None
    for tile in permuted_tiles:
        tile.set_valid_neighbors(permuted_tiles)
        if (tile.image_path == "../../base_tiles/tests/blank.png" and
                tile.sides == {"up": "0", "right": "0", "down": "0", "left": "0"}):
            blank = tile
        elif (tile.image_path == "../../base_tiles/tests/T.png" and
                tile.sides == {"up": "1", "right": "1", "down": "0", "left": "1"}):
            t = tile
        elif (tile.image_path == "../../base_tiles/tests/b_i.png" and
                tile.sides == {"up": "0", "right": "1", "down": "0", "left": "1"}):
            circle1 = tile
        elif (tile.image_path == "../../base_tiles/tests/4.png" and
                tile.sides == {"up": "011", "right": "121", "down": "110", "left": "000"}):
            pcb1 = tile
        elif (tile.image_path == "../../base_tiles/tests/5.png" and
                tile.sides == {"up": "011", "right": "111", "down": "111", "left": "110"}):
            pcb2 = tile

    assert blank is not None
    assert t is not None
    assert circle1 is not None
    assert pcb1 is not None
    assert pcb2 is not None

    assert len(blank.valid_neighbors['up']) == 3
    assert len(blank.valid_neighbors['left']) == 3
    assert len(blank.valid_neighbors['right']) == 3
    assert len(blank.valid_neighbors['down']) == 3

    assert len(t.valid_neighbors['up']) == 4
    assert len(t.valid_neighbors['left']) == 4
    assert len(t.valid_neighbors['right']) == 4
    assert len(t.valid_neighbors['down']) == 3

    assert len(circle1.valid_neighbors['up']) == 3
    assert len(circle1.valid_neighbors['left']) == 4
    assert len(circle1.valid_neighbors['right']) == 4
    assert len(circle1.valid_neighbors['down']) == 3

    assert len(pcb1.valid_neighbors['up']) == 2
    assert len(pcb1.valid_neighbors['left']) == 1
    assert len(pcb1.valid_neighbors['right']) == 1
    assert len(pcb1.valid_neighbors['down']) == 2

    assert len(pcb2.valid_neighbors['up']) == 2
    assert len(pcb2.valid_neighbors['left']) == 2
    assert len(pcb2.valid_neighbors['right']) == 2
    assert len(pcb2.valid_neighbors['down']) == 2

def test_copy_tile_and_rotate_0_times(setup_tile_blank):
    new_tile = setup_tile_blank.copy_tile_and_rotate(0)
    assert new_tile is not setup_tile_blank
    assert new_tile.sides == setup_tile_blank.sides

def test_copy_tile_and_rotate_1_time(setup_tile_symmetric):
    new_tile = setup_tile_symmetric.copy_tile_and_rotate(1)
    assert new_tile is not setup_tile_symmetric
    assert new_tile.sides != setup_tile_symmetric.sides
    assert new_tile.sides['up'] == setup_tile_symmetric.sides['left']
    assert new_tile.sides['right'] == setup_tile_symmetric.sides['up']
    assert new_tile.sides['down'] == setup_tile_symmetric.sides['right']
    assert new_tile.sides['left'] == setup_tile_symmetric.sides['down']

def test_copy_tile_and_rotate_2_time(setup_tile_symmetric):
    new_tile = setup_tile_symmetric.copy_tile_and_rotate(2)
    assert new_tile is not setup_tile_symmetric
    assert new_tile.sides != setup_tile_symmetric.sides
    assert new_tile.sides['up'] == setup_tile_symmetric.sides['down']
    assert new_tile.sides['right'] == setup_tile_symmetric.sides['left']
    assert new_tile.sides['down'] == setup_tile_symmetric.sides['up']
    assert new_tile.sides['left'] == setup_tile_symmetric.sides['right']

def test_copy_tile_and_rotate_3_time(setup_tile_symmetric):
    new_tile = setup_tile_symmetric.copy_tile_and_rotate(3)
    assert new_tile is not setup_tile_symmetric
    assert new_tile.sides != setup_tile_symmetric.sides
    assert new_tile.sides['up'] == setup_tile_symmetric.sides['right']
    assert new_tile.sides['right'] == setup_tile_symmetric.sides['down']
    assert new_tile.sides['down'] == setup_tile_symmetric.sides['left']
    assert new_tile.sides['left'] == setup_tile_symmetric.sides['up']

def test_copy_tile_and_rotate_deepcopy(setup_tile_blank):
    new_tile = setup_tile_blank.copy_tile_and_rotate(0)
    assert new_tile.sides == setup_tile_blank.sides
    assert new_tile.sides is not setup_tile_blank.sides
    assert new_tile is not setup_tile_blank
