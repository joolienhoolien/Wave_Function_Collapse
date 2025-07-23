"""
Responsible for:
    data:
    - x, y coordinates in it's parent grid
    - set of current options for which tile it can be
    - collapsed state
    - if collapsed, it's tile
    - image or image path
    func:
    - Collapsing itself into a tile
        - If given a tile to collapse into, picks that one
        - Else, randomly choose from current options
        - updating image or image path
"""
class Node:
    def __init__(self, x, y, tile_options):
        self.x = x
        self.y = y
        self.tile_options = set(tile_options)
        self.collapsed = False

        #Unsure about these currently
        self.image = None
        self.image_path = None
        self.tile = None

    def collapse(self):
        pass

    #Get/set
    def is_collapsed(self):
        return self.collapsed