## Project: pyEnkido
## Module: Tank entity
## Author: Salwan

import pygame
import pyenkido.entity
import battlecity.entities.cannon_shell
from battlecity.defs import *
from pyenkido.particle_system import *

# Settings
TANK_MOVEMENT_DELAY = 2
SHIELD_FRAME_DELAY = 1
CANNON_SHELL_TIMEOUT = 20

# Tank states
TANK_NORMAL = 0
TANK_SHIELDED = 1

# Sliding period
SlidingPeriod = 30

class Tank(pyenkido.entity.Entity):
    def __init__(self, bitmap, level):
        super(Tank, self).__init__()
        self.bitmap = bitmap
        self.level = level
        self.images = [self.bitmap.subsurface(GameData[GAME_PLACEHOLDER_16])]
        setTankPalette(self.images[0], TANK_PAL_NONE)
        self.rect = pygame.Rect(0, 0, 16, 16)
        self.rectBounds = pygame.Rect(16, 16, 208, 208)
    
        self.direction = TANK_UP
        self.movement = 0
        self.isSpawned = False

        self.shieldFrames = 0
        self.shieldImages = []
        rc = GameData[TANK_SHIELD_EFFECT].copy()
        for i in range(0, 2):
            self.shieldImages.append(self.bitmap.subsurface(rc))
            rc.left += 16
        self.currentShieldFrame = 0
        self.shieldTicks = 0

        self.cannonShells = {}
        self.cannonShells[TANK_UP] = self.bitmap.subsurface(GameData[TANK_CANNON_SHELL_UP])
        self.cannonShells[TANK_DOWN] = self.bitmap.subsurface(GameData[TANK_CANNON_SHELL_DOWN])
        self.cannonShells[TANK_LEFT] = self.bitmap.subsurface(GameData[TANK_CANNON_SHELL_LEFT])
        self.cannonShells[TANK_RIGHT] = self.bitmap.subsurface(GameData[TANK_CANNON_SHELL_RIGHT])
        self.cannonShellTicks = 0
        self.cannonShellSpeedBoost = 0
        self.cannonShellTimeOut = CANNON_SHELL_TIMEOUT
        self.cannonShellsNumber = 1
        self.lastCannonShells = []

        self.state = [TANK_NORMAL]
        self.speed = 30.0 # pixels per second
        self.speedAccum = 0.0

        self.type = ENTITY_TYPE_TANK
        self.tankType = ENTITY_TYPE_TANK

        self.explosionSound = pyenkido.sound.load_sound("res/sounds", "big_explosion.ogg")

        # Ice effect
        self.isSliding = False
        self.slidingTicks = 0

    def update(self):
        # Drawing the tank
        self.image = self.images[self.direction + self.movement]
        # Check for shield
        if TANK_SHIELDED in self.state:
            if self.shieldFrames > 0:
                self.shieldTicks += 1
                if self.shieldTicks > SHIELD_FRAME_DELAY:
                    self.currentShieldFrame = 1 - self.currentShieldFrame
                    self.shieldFrames -= 1
                    self.shieldTicks = 0
            else:
                self.currentShieldFrame = 0
                self.shieldFrames = 0
                self.state.remove(TANK_SHIELDED)
        # Decrement cannon counter
        if self.cannonShellTicks > 0:
            self.cannonShellTicks -= 1
        # Eleminate dead shells
        if len(self.lastCannonShells) > 0:
            for c in self.lastCannonShells:
                if not c.isAlive():
                    self.lastCannonShells.remove(c)

        # Check for sliding
        if self.isSliding:
            # Is this tank still on ice?
            if len(self.level.collideIce(self.rect)) > 0:
                self.slidingTicks -= 1
                if self.slidingTicks < 1:
                    self.isSliding = False
                    self.slidingTicks = 0
                self.move()
            else:
                self.isSliding = False
                self.slidingTicks = 0

    def postDraw(self, screen):
        if TANK_SHIELDED in self.state:
            screen.blit(self.shieldImages[self.currentShieldFrame], (self.rect.left, self.rect.top))

    def fire(self):
        if self.canFire():
            self.cannonShellTicks = self.cannonShellTimeOut
            pos = self.rect.center
            if self.direction == TANK_UP:
                pos = (pos[0] - 2, pos[1] - 10) # hard coded fire points
            elif self.direction == TANK_DOWN:
                pos = (pos[0] - 2, pos[1] + 6)
            elif self.direction == TANK_LEFT:
                pos = (pos[0] - 10, pos[1] - 2)
            elif self.direction == TANK_RIGHT:
                pos = (pos[0] + 6, pos[1] - 2)
            shell = battlecity.entities.cannon_shell.CannonShell(self.level, self, self.cannonShells, pos, self.direction)
            shell.speed += self.cannonShellSpeedBoost
            self.level.spawnEntity(shell)
            self.lastCannonShells.append(shell)

    def canFire(self):
        if self.cannonShellTicks == 0 and len(self.lastCannonShells) < self.cannonShellsNumber:
            return True
        else:
            return False

    def move(self):
        validate_tanks = True
        # If tank already overlaps another tank, allow it to move anyway rather than getting stuck
        if self.isOverlapTank():
            validate_tanks = False

        # Actual movement
        move_rect = self.rect.copy()
        self.speedAccum += TIME_STEP
        while self.speedAccum > (1.0 / self.speed):
            self.speedAccum -= 1.0 / self.speed
            self.movement = 1 - self.movement
            if self.direction == TANK_UP:
                move_rect.top -= 1
            elif self.direction == TANK_DOWN:
                move_rect.top += 1
            elif self.direction == TANK_LEFT:
                move_rect.left -= 1
            elif self.direction == TANK_RIGHT:
                move_rect.left += 1

        if self.isMoveValid(move_rect, validate_tanks):
            self.rect = move_rect

    def isMoveValid(self, future_rect, validate_tanks = True):
        # Check validity of future position
        # - Against screen bounds
        if not self.rectBounds.contains(future_rect):
            return False
        # - Against map tiles
        coll_list = self.level.collideMap(future_rect)
        if len(coll_list) > 0:
            # Trees don't count
            for t in coll_list:
                if t.type != TILE_TYPE_TREE and t.type != TILE_TYPE_ICE:
                    return False
        # - Against other tanks
        if validate_tanks:
            coll_list = self.level.collideEntities(future_rect)
            if len(coll_list) > 0:
                for c in coll_list:
                    if (c.type == ENTITY_TYPE_TANK or c.type == ENTITY_TYPE_PLAYER_TANK) and c is not self:
                        return False
        # Everything is OK
        return True

    def isOverlapTank(self):
        coll_list = self.level.collideEntities(self.rect)
        if len(coll_list) > 0:
            for c in coll_list:
                if (c.type == ENTITY_TYPE_TANK or c.type == ENTITY_TYPE_PLAYER_TANK) and c is not self:
                    return True
        return False

    def alignToGrid(self):
        center = self.rect.center
        nearest = (round(float(center[0] - 16) / 8.0), round(float(center[1] - 16) / 8.0))
        nearest_pos = (16 + nearest[0] * 8, 16 + nearest[1] * 8)
        if self.isMoveValid(pygame.Rect(nearest_pos[0] - 8, nearest_pos[1] - 8, 16, 16), True):
            self.rect.center = nearest_pos

    def giveShield(self, frame_count):
        self.state.append(TANK_SHIELDED)
        self.shieldFrames = frame_count

    def hasShield(self):
        return TANK_SHIELDED in self.state

    def spawned(self):
        self.image = self.images[0]
        if self.controller:
            self.controller.activate()
        self.isSpawned = True

    def started_moving(self):
        if self.isSliding:
            self.isSliding = False
            self.slidingTicks = 0

    def stopped_moving(self):
        # Is this tank on ice?
        if len(self.level.collideIce(self.rect)) > 0:
            self.isSliding = True
            self.slidingTicks = SlidingPeriod

    def setLeft(self):
        if self.direction == TANK_UP or self.direction == TANK_DOWN:
            self.alignToGrid()
        self.direction = TANK_LEFT

    def setRight(self):
        if self.direction == TANK_UP or self.direction == TANK_DOWN:
            self.alignToGrid()
        self.direction = TANK_RIGHT

    def setUp(self):
        if self.direction == TANK_LEFT or self.direction == TANK_RIGHT:
            self.alignToGrid()
        self.direction = TANK_UP

    def setDown(self):
        if self.direction == TANK_LEFT or self.direction == TANK_RIGHT:
            self.alignToGrid()
        self.direction = TANK_DOWN

    def killed(self):
        self.explosionSound.play()
        self.spawnBigExplosion()
        # TEMP: Testing simply particle system
        p = ParticleSystem(self.rect.center, TIME_STEP, 10, [(255, 255, 255),(48,80,128),(188,188,188)])
        self.level.scene.spawnParticleSystem(p)

    def spawnBigExplosion(self):
        explosion = battlecity.entities.explosion.BigExplosion(self.level.bitmap, self.rect.center)
        self.level.spawnEntity(explosion)

    def takeDamage(self, area = None, amount = 0):
        if TANK_SHIELDED not in self.state:
            self.kill()

    def setStopWatch(self, ticks):
        pass

