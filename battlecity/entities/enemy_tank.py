## Project: BattleCity
## Module: Enemy Tank entity
## Author: Salwan

import pygame
import pyenkido.entity
from battlecity.defs import *
import battlecity.entities.tank

SHIELD_COLOR_PERIOD = 2

Shields = {}
Shields[ENEMY_SHIELD_NONE] = []
Shields[ENEMY_SHIELD_ITEM] = [(TANK_PAL_RED, TANK_PAL_METAL)]
Shields[ENEMY_SHIELD_FULL] = [(TANK_PAL_GREEN, TANK_PAL_METAL), (TANK_PAL_ORANGE, TANK_PAL_METAL), (TANK_PAL_GREEN, TANK_PAL_ORANGE)]
Shields[ENEMY_SHIELD_FULL_ITEM] = [(TANK_PAL_RED, TANK_PAL_METAL), (TANK_PAL_ORANGE, TANK_PAL_METAL), (TANK_PAL_GREEN, TANK_PAL_ORANGE)]

class EnemyTank(battlecity.entities.tank.Tank):
    def __init__(self, bitmap, level, tank_type, tank_shield, enemy_textures):
        super(EnemyTank, self).__init__(bitmap, level)
        self.enemyTextures = enemy_textures
        self.direction = TANK_DOWN
        self.pimages = {}
        for j in range(0, 4):
            t = TANK_PAL_METAL + j
            self.pimages[t] = []
            rc = pygame.rect.Rect(0, j * 16, 16, 16)
            for i in range(0, 8):
                surface = self.enemyTextures[tank_type].subsurface(rc)
                self.pimages[t].append(surface)
                rc.left += 16
        self.shield = list(Shields[tank_shield])
        self.shieldTicks = SHIELD_COLOR_PERIOD
        self.currentColor = 0
        if len(self.shield) > 0:
            self.images = self.pimages[self.shield[0][self.currentColor]]
        else:
            self.images = self.pimages[TANK_PAL_METAL]
        self.image = self.images[0]

        self.tankType = tank_type
        if tank_type == GAME_ENEMY_1_TANK: # Normal
            self.speed += 10.0
        elif tank_type == GAME_ENEMY_2_TANK: # Quickcy
            self.speed += 35.0
        elif tank_type == GAME_ENEMY_3_TANK: # Stud
            self.speed += 15.0
            self.cannonShellSpeedBoost = 50
        elif tank_type == GAME_ENEMY_4_TANK: # Tough-o-tank
            #self.speed -= 5.0
            pass

    def update(self):
        if len(self.shield) > 0:
            self.shieldTicks -= 1
            if self.shieldTicks <= 0:
                self.shieldTicks = SHIELD_COLOR_PERIOD
                self.currentColor = 1 - self.currentColor
                self.images = self.pimages[self.shield[0][self.currentColor]]
        super(EnemyTank, self).update()

    def killed(self):
        super(EnemyTank, self).killed()

    def takeDamage(self, area = None, amount = 0):
        if len(self.shield) > 0 and amount == 0:
            if self.shield[0][0] == TANK_PAL_RED:
                self.level.spawnItem()
            del self.shield[0]
            self.shieldTicks = 0
            if len(self.shield) == 0:
                self.images = self.pimages[TANK_PAL_METAL]
        else:
            self.kill()

    def setStopWatch(self, ticks):
        if self.controller != None:
            self.controller.setStopWatch(ticks)

