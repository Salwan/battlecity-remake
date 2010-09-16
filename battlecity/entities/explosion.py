## Project: BattleCity
## Module: Explosions
## Author: Salwan

import pygame
import pyenkido.entity
from battlecity.defs import *

# enum frame transition delay
IMPACT_EXPLOSION_FRAME_DELAY = 4
BIG_EXPLOSION_FRAME_DELAY = 6

class ImpactExplosion(pyenkido.entity.Entity):
    def __init__(self, bitmap, position):
        super(ImpactExplosion, self).__init__()
        self.bitmap = bitmap
        self.pos = position
        self.images = []
        self.images.append(self.bitmap.subsurface(GameData[IMPACT_EXPLOSION_1]))
        self.images.append(self.bitmap.subsurface(GameData[IMPACT_EXPLOSION_2]))
        self.images.append(self.bitmap.subsurface(GameData[IMPACT_EXPLOSION_3]))
        self.currentFrame = 0
        self.image = self.images[0]
        self.rect = pygame.rect.Rect(self.pos[0] - 8, self.pos[1] - 8, 16, 16)
        self.ticks = 0

    def update(self):
        self.ticks += 1
        if self.ticks >= IMPACT_EXPLOSION_FRAME_DELAY:
            self.ticks = 0
            self.currentFrame += 1
            if self.currentFrame >= len(self.images):
                self.kill()
                return
            self.image = self.images[self.currentFrame]

    def postDraw(self, screen):
        super(ImpactExplosion, self).postDraw(screen)
        screen.blit(self.images[self.currentFrame], self.rect.topleft)

class BigExplosion(pyenkido.entity.Entity):
    def __init__(self, bitmap, position):
        super(BigExplosion, self).__init__()
        self.bitmap = bitmap
        self.pos = position
        self.images = []
        self.images.append(self.bitmap.subsurface(GameData[IMPACT_EXPLOSION_1]))
        self.images.append(self.bitmap.subsurface(GameData[IMPACT_EXPLOSION_2]))
        self.images.append(self.bitmap.subsurface(GameData[IMPACT_EXPLOSION_3]))
        self.images.append(self.bitmap.subsurface(GameData[IMPACT_EXPLOSION_4]))
        self.images.append(self.bitmap.subsurface(GameData[IMPACT_EXPLOSION_5]))
        self.currentFrame = 0
        self.image = self.images[0]
        self.rect = pygame.rect.Rect(self.pos[0] - 8, self.pos[1] - 8, 16, 16)
        self.ticks = 0

    def update(self):
        self.ticks += 1
        if self.ticks >= BIG_EXPLOSION_FRAME_DELAY:
            self.ticks = 0
            self.currentFrame += 1
            if self.currentFrame >= len(self.images):
                self.kill()
                return
            self.image = self.images[self.currentFrame]
            if self.currentFrame < 3:
                self.rect = pygame.rect.Rect(self.pos[0] - 8, self.pos[1] - 8, 16, 16)
            else:
                self.rect = pygame.rect.Rect(self.pos[0] - 16, self.pos[1] - 16, 32, 32)

    def postDraw(self, screen):
        super(BigExplosion, self).postDraw(screen)
        screen.blit(self.images[self.currentFrame], self.rect.topleft)

