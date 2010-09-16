## Project: pyEnkido
## Module: Shovel Action, a non-visual entity that effects the map
## Author: Salwan

import os, pygame
import pyenkido.entity
from battlecity.defs import *

STONE_REINFORCE_BASE_TIME = 8 * 60
ALTERNATE_REINFORCE_BASE_TIME = 4 * 60
ALTERNATE_REINFORCE_RATE = 30

class ShovelAction(pyenkido.entity.Entity):
    def __init__(self, level, map):
        super(ShovelAction, self).__init__()
        self.ticks = 0
        self.level = level
        self.map = map
        # Reinforce the wall by stone
        self.wall = [(11,25),(11,24),(11,23),(12,23),(13,23),(14,23),(14,24),(14,25)]
        self.image = pygame.Surface((1,1))
        self.image.fill((255, 0, 255))
        self.image.set_colorkey((255, 0, 255))
        self.rect = pygame.rect.Rect(0, 0, 1, 1)
        for i in self.wall:
            self.map.clearTile(i)
            self.map.createTile(i, TILE_TYPE_STONE)
        self.blinkTicks = 0
        self.blinkState = False

    def update(self):
        self.ticks += 1
        if self.ticks > STONE_REINFORCE_BASE_TIME:
            if self.ticks < STONE_REINFORCE_BASE_TIME + ALTERNATE_REINFORCE_BASE_TIME:
                self.blinkTicks += 1
                if self.blinkTicks > ALTERNATE_REINFORCE_RATE:
                    self.blinkTicks = 0
                    self.blinkState = not self.blinkState
                    self.setWall(self.blinkState)
            else:
                self.setWall(False)
                self.kill()

    def setWall(self, stone):
        tile_type = TILE_TYPE_STONE
        if not stone:
            tile_type = TILE_TYPE_BRICK
        for i in self.wall:
            self.map.clearTile(i)
            self.map.createTile(i, tile_type)

