## Project: pyEnkido
## Module: Stone Tile
## Author: Salwan

import pygame
from battlecity.defs import *
import battlecity.entities.tile

class Stone(battlecity.entities.tile.Tile):
    def __init__(self, group, bitmap, at, layer = 0):
        self.bitmap = bitmap
        super(Stone, self).__init__(group, bitmap.subsurface(TilesData[TILE_TYPE_STONE]), pygame.Rect(0, 0, 16, 16), TILE_TYPE_STONE, layer)
        self.setPosition(at)

        # Determine if this is a base wall
#        aat = (at[0] / 2, at[1] / 2)
#        if at in EAGLE_ADJ:
#            self.eagleWall = True
#        else:
        self.eagleWall = False

    def update(self):
        pass

    def takeDamage(self, area = None, amount = 0):
        if amount == GAME_PLAYER_TANK_4:
            super(Stone,self).takeDamage()

        #if self.eagleWall:
        #    print "YOU JUST HIT A FUCKING BASE WALL MADE OF STONE!!!"

    def isEagleWall(self):
        return self.eagleWall

    def getObjectCoords(self, pos):
        return ((pos[0] - 16) / 16, (pos[1] - 16) / 16)
