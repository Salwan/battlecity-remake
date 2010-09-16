## Project: pyEnkido
## Module: Item Entity
## Author: Salwan

import os, pygame
import pyenkido.entity
from battlecity.defs import *

class ItemEntity(pyenkido.entity.Entity):
    def __init__(self, bitmap, position, type, layer = 0):
        super(ItemEntity, self).__init__()
        self.layer = layer
        self.type = type
        self.bitmap = bitmap
        self.itemImage = self.bitmap.subsurface(GameData[type])
        self.image = pygame.Surface((1,1))
        self.image.set_colorkey((255, 0, 255))
        self.image.fill((255, 0, 255))
        self.rect = pygame.rect.Rect(position[0] + 2, position[1], 12, 12)
        self.ticks = 0
        self.blinkState = True
        # lives for 10 seconds
        self.life = 60 * 10

    def update(self):
        self.life -= 1
        if self.life <= 0:
            self.kill()
        self.ticks += 1
        if self.ticks > 15:
            self.ticks = 0
            self.blinkState = not self.blinkState

    def postDraw(self, screen):
        if self.blinkState:
            screen.blit(self.itemImage, self.rect.topleft)
