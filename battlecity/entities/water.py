## Project: pyEnkido
## Module: Water Tile
## Author: Salwan

import pygame
from battlecity.defs import *
import battlecity.entities.tile

class Water(battlecity.entities.tile.Tile):
    def __init__(self, group, bitmap, at, layer = 0):
        self.bitmap = bitmap
        super(Water, self).__init__(group, bitmap.subsurface(TilesData[TILE_TYPE_WATER]), pygame.Rect(0, 0, 16, 16), TILE_TYPE_WATER, layer)
        self.setPosition(at)
        self.waterImages = [self.image.subsurface(0, 0, 8, 8), self.image.subsurface(8, 0, 8, 8)]
        self.currentImage = 0
        self.image = self.waterImages[self.currentImage]
        self.ticks = 0

    def update(self):
        self.ticks += 1
        if self.ticks > 60:
            self.currentImage = 1 - self.currentImage
            self.image = self.waterImages[self.currentImage]
            self.ticks = 0


