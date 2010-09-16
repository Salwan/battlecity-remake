## Project: BattleCity
## Module: cannon shell
## Author: Salwan

import pygame
import pyenkido.entity
import battlecity.entities.explosion
from battlecity.defs import *

class CannonShell(pyenkido.entity.Entity):
    def __init__(self, level, shooter, cannon_shell_surfaces, position, direction):
        super(CannonShell, self).__init__()
        self.level = level
        self.shooter = shooter
        self.images = cannon_shell_surfaces
        self.direction = direction
        self.image = self.images[self.direction]
        self.rect = self.image.get_rect()
        self.rect.topleft = position
        self.rectBounds = pygame.rect.Rect(16, 16, 208, 208)
        self.speed = 130.0
        self.speedAccum = 0.0
        self.type = ENTITY_TYPE_CANNON_SHELL

        self.impactSound = pyenkido.sound.load_sound("res/sounds", "solid_impact.ogg")

    def update(self):
        super(CannonShell, self).update()
        self.speedAccum += TIME_STEP
        while self.speedAccum > (1.0 / self.speed):
            self.speedAccum -= 1.0 / self.speed
            if self.direction == TANK_UP:
                self.rect.top -= 1
            elif self.direction == TANK_DOWN:
                self.rect.top += 1
            elif self.direction == TANK_LEFT:
                self.rect.left -= 1
            elif self.direction == TANK_RIGHT:
                self.rect.left += 1

        # Check for collision
        # - Against screen bounds
        if not self.rectBounds.contains(self.rect):
            self.spawnImpactExplosion()
            self.kill()
        # - Against map tiles
        coll_list = self.level.collideCannonShellMap(self.rect)
        tankLevel = 0
        if self.shooter.type == ENTITY_TYPE_PLAYER_TANK:
            tankLevel = self.shooter.tankLevel
        if len(coll_list) > 0:
            # Trees don't count, nor water, nor ice
            for t in coll_list:
                if t.type not in (TILE_TYPE_TREE, TILE_TYPE_WATER, TILE_TYPE_ICE):
                    self.spawnImpactExplosion()
                    if t.type == TILE_TYPE_BRICK or t.type == TILE_TYPE_STONE:
                        center = self.rect.center
                        if self.direction == TANK_LEFT or self.direction == TANK_RIGHT:
                            t.takeDamage(pygame.rect.Rect(center[0] - 2, center[1] - 7, 4, 14), tankLevel)
                        elif self.direction == TANK_UP or self.direction == TANK_DOWN:
                            t.takeDamage(pygame.rect.Rect(center[0] - 7, center[1] - 2, 14, 4), tankLevel)
                    elif t.type == TILE_TYPE_EAGLE:
                        self.spawnImpactExplosion()
                        t.takeDamage(self.level)
                    self.kill()
        # - Against other tanks
        coll_list = self.level.collideEntities(self.rect)
        if len(coll_list) > 0:
            for c in coll_list:
                if c != self:
                    if self.shooter.type == ENTITY_TYPE_TANK and c.type == ENTITY_TYPE_PLAYER_TANK:
                        if not self.level.godMode:
                            self.spawnImpactExplosion()
                            c.takeDamage()
                            self.kill()
                    elif self.shooter.type == ENTITY_TYPE_PLAYER_TANK and c.type == ENTITY_TYPE_TANK:
                        self.spawnImpactExplosion()
                        c.takeDamage()
                        if not c.isAlive():
                            self.level.addFragScore(c.tankType, c.rect)
                        self.kill()
                    elif c.type == ENTITY_TYPE_CANNON_SHELL:
                        self.spawnImpactExplosion()
                        c.kill()
                        self.kill()

    def spawnImpactExplosion(self):
        explosion = battlecity.entities.explosion.ImpactExplosion(self.level.bitmap, self.rect.center)
        self.level.spawnEntity(explosion)

    def preDraw(self, screen):
        super(CannonShell, self).preDraw(screen)

    def postDraw(self, screen):
        super(CannonShell, self).postDraw(screen)
        screen.blit(self.image, self.rect.topleft)

    def spawned(self):
        super(CannonShell, self).spawned()

    def killed(self):
        if self.shooter.type == ENTITY_TYPE_PLAYER_TANK:
            self.impactSound.play()

