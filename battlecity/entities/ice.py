## Project: pyEnkido
## Module: Ice Tile
## Author: Salwan

import pygame
from battlecity.defs import *
import battlecity.entities.tile

class Ice(battlecity.entities.tile.Tile):
    def __init__(self, group, bitmap, at, layer = 0):
        self.bitmap = bitmap
        super(Ice, self).__init__(group, bitmap.subsurface(TilesData[TILE_TYPE_ICE]), pygame.Rect(0, 0, 16, 16), TILE_TYPE_ICE, layer)
        self.setPosition(at)
        self.iceImage = self.image
        # HACK: Use dummy transparent pixel for pygame's sprite
        self.image = pygame.Surface((1,1))
        self.image.fill((255, 0, 255))
        self.image.set_colorkey((255, 0, 255))

    def update(self):
        pass
    
    def preDraw(self, screen):
        screen.blit(self.iceImage, self.rect.topleft)



