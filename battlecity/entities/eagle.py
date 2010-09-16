## Project: pyEnkido
## Module: Eagle Tile
## Author: Salwan

import pygame, pyenkido
from battlecity.defs import *
import battlecity.entities.tile
import battlecity.entities.explosion

class Eagle(battlecity.entities.tile.Tile):
    def __init__(self, group, bitmap, rect, type, layer = 0):
        self.bitmap = bitmap
        super(Eagle, self).__init__(group, bitmap.subsurface(TilesData[TILE_TYPE_EAGLE]), rect, TILE_TYPE_EAGLE, layer)
        self.setPosition(rect.topleft)
        self.images = {}
        self.images["eagle"] = self.bitmap.subsurface(TilesData[TILE_TYPE_EAGLE])
        self.images["destroyed"] = self.bitmap.subsurface(TilesData[TILE_TYPE_EAGLE_DESTROYED])
        self.image = self.images["eagle"]
        self.sound = pyenkido.sound.load_sound("res/sounds", "base_explosion.ogg")
        self.destroyed = False

    def update(self):
        pass

    def takeDamage(self, level):
        if not self.destroyed:
            self.sound.play()
            self.image = self.images["destroyed"]
            self.destroyed = True
            explosion = battlecity.entities.explosion.BigExplosion(level.bitmap, self.rect.center)
            level.spawnEntity(explosion)
            level.setGameOver()
