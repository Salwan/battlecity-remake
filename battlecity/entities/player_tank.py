## Project: BattleCity
## Module: Player Tank entity
## Author: Salwan

import pygame
import pyenkido.entity
import pyenkido.sound
from battlecity.defs import *
from battlecity.entities.tank import *

PLAYER_START_SHIELDED_PERIOD = 92 # 92 frames

# (Speed, CannonShellSpeedBoost, CannonShellTimeOut, ConcurrentShellNumber)
PlayerTankProperties = {
    GAME_PLAYER_TANK_1: (35.0, 0.0, 15, 1),
    GAME_PLAYER_TANK_2: (40.0, 80.0, 12, 1),
    GAME_PLAYER_TANK_3: (45.0, 120.0, 10, 1),
    GAME_PLAYER_TANK_4: (45.0, 200.0, 6, 2),
}

class PlayerTank(Tank):
    def __init__(self, bitmap, level, tank_level, player_number, player_textures):
        super(PlayerTank, self).__init__(bitmap, level)
        self.playerNum = player_number
        self.playerTextures = player_textures
        self.pimages = {}
        p = GAME_PLAYER_TANK_1
        for j in range(0, 4):
            t = p + j
            self.pimages[t] = []
            rc = pygame.Rect(0, j * 16, 16, 16)
            for i in range(0, 8):
                surface = self.playerTextures[self.playerNum].subsurface(rc)
                self.pimages[t].append(surface)
                rc.left += 16
        self.tankLevel = tank_level
        self.images = self.pimages[self.tankLevel]
        self.image = self.images[0]
        self.type = ENTITY_TYPE_PLAYER_TANK
        self.speed = PlayerTankProperties[self.tankLevel][0]
        self.cannonShellSpeedBoost = PlayerTankProperties[self.tankLevel][1]
        self.cannonShellTimeOut = PlayerTankProperties[self.tankLevel][2]
        self.cannonShellsNumber = PlayerTankProperties[self.tankLevel][3]
        
        self.tankType = TANK_TYPE_PLAYER1

        self.sounds = {}
        self.sounds["idle"] = pyenkido.sound.load_sound("res/sounds", "tank_idle.ogg")
        self.sounds["moving"] = pyenkido.sound.load_sound("res/sounds", "tank_moving.ogg")

        # Using mixer channel 1
        self.channel = pygame.mixer.Channel(1)

    def update(self):
        super(PlayerTank, self).update()

    def spawned(self):
        super(PlayerTank, self).spawned()
        self.giveShield(PLAYER_START_SHIELDED_PERIOD)
        self.channel.play(self.sounds["idle"], -1)

    def move(self):
        super(PlayerTank, self).move()

    def started_moving(self):
        super(PlayerTank, self).started_moving()
        self.channel.play(self.sounds["moving"], -1)

    def stopped_moving(self):
        super(PlayerTank, self).stopped_moving()
        self.channel.play(self.sounds["idle"], -1)

    def killed(self):
        super(PlayerTank, self).killed()
        self.channel.stop()

    def upgradeTank(self):
        if self.tankLevel < GAME_PLAYER_TANK_4:
            self.tankLevel += 1
            self.images = self.pimages[self.tankLevel]
            self.speed = PlayerTankProperties[self.tankLevel][0]
            self.cannonShellSpeedBoost = PlayerTankProperties[self.tankLevel][1]
            self.cannonShellTimeOut = PlayerTankProperties[self.tankLevel][2]
            self.cannonShellsNumber = PlayerTankProperties[self.tankLevel][3]

    def game_paused(self):
        self.channel.pause()

    def game_resumed(self):
        self.channel.unpause()

    def getTankLevel(self):
        return self.tankLevel



