## Project: pyEnkido
## Module: Tree Tile
## Author: Salwan

import pygame
from battlecity.defs import *
import battlecity.entities.tile

class Tree(battlecity.entities.tile.Tile):
    def __init__(self, group, bitmap, at, layer = 10):
        self.bitmap = bitmap
        super(Tree, self).__init__(group, bitmap.subsurface(TilesData[TILE_TYPE_TREE]), pygame.Rect(0, 0, 16, 16), TILE_TYPE_TREE, layer)
        self.setPosition(at)

    def update(self):
        pass


