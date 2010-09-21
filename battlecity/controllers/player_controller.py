## Project: BattleCity
## Module: player controller
## Author: Salwan

import pygame
import pyenkido.entity
import pyenkido.controller
from battlecity.defs import *

FREEZE_PENALTY_PERIOD = 60 * 3
FREEZE_BLINK_RATE = 10

class PlayerController(pyenkido.controller.Controller):
    def __init__(self):
        super(PlayerController, self).__init__()
        self.downMoveKeys = []
        self.fireKeysDown = [] 
        self.setPlayerControls(1)
        self.active = True
        self.frozen = False
        self.freezeTicks = FREEZE_PENALTY_PERIOD
        self.freezeBlinkRate = FREEZE_BLINK_RATE
        self.freezeBlink = 1
        self.score = 0               

        # Audio
        self.sounds = {}
        self.sounds["fire"] = pyenkido.sound.load_sound("res/sounds", "tank_fire.ogg")
        self.channel = pygame.mixer.Channel(2)        
        
    def setPlayerControls(self, player_number):
        n = player_number
        self.controls = PlayerKeyboardControls[n]
        self.movementKeys = [
                self.controls[CONTROL_UP], 
                self.controls[CONTROL_DOWN], 
                self.controls[CONTROL_LEFT], 
                self.controls[CONTROL_RIGHT]
            ]
        self.fireKeys = self.controls[CONTROL_FIRE]

    def addScore(self, score):
        self.score += score
        
    def attached_to_entity(self, entity):
        super(PlayerController, self).attached_to_entity(entity)
        # Update input controls based on player number
        if entity.type == ENTITY_TYPE_PLAYER_TANK:
            self.setPlayerControls(entity.playerNum)
        

    def update(self):
        if self.frozen:
            self.freezeTicks -= 1
            self.freezeBlinkRate -= 1
            if self.freezeBlinkRate <= 0:
                self.freezeBlinkRate = FREEZE_BLINK_RATE
                self.freezeBlink = 1 - self.freezeBlink
            if self.freezeTicks <= 0:
                self.frozen = False
            return

        if not self.entity or not self.active:
            return

        if len(self.downMoveKeys) > 0:
            self.entity.move()
        if len(self.fireKeysDown) > 0:
            if self.entity.canFire():
                self.channel.play(self.sounds["fire"], 0)
                self.entity.fire()

    def key_down(self, key):
        if not self.entity or not self.active:
            return

        # Fire
        if key in self.fireKeys:
            if key not in self.fireKeysDown:
                self.fireKeysDown.append(key)
            if self.entity.canFire():
                self.channel.play(self.sounds["fire"], 0)
                self.entity.fire()

        # Movement
        if key in self.movementKeys and key not in self.downMoveKeys:
            self.downMoveKeys.append(key)

        if len(self.downMoveKeys) > 0:
            self.entity.started_moving()

        if len(self.downMoveKeys) > 0:
            k = self.downMoveKeys[-1]
            if k == self.controls[CONTROL_UP]:
                self.entity.setUp()
            elif k == self.controls[CONTROL_DOWN]:
                self.entity.setDown()
            elif k == self.controls[CONTROL_LEFT]:
                self.entity.setLeft()
            elif k == self.controls[CONTROL_RIGHT]:
                self.entity.setRight()

    def key_up(self, key):
        if not self.active:
            return

        if key in self.fireKeysDown:
            self.fireKeysDown.remove(key)
        
        if key in self.downMoveKeys:
            self.downMoveKeys.remove(key)
            
        if len(self.downMoveKeys) > 0:
            k = self.downMoveKeys[-1]
            if k == self.controls[CONTROL_UP]:
                self.entity.setUp()
            elif k == self.controls[CONTROL_DOWN]:
                self.entity.setDown()
            elif k == self.controls[CONTROL_LEFT]:
                self.entity.setLeft()
            elif k == self.controls[CONTROL_RIGHT]:
                self.entity.setRight()
        else:
            self.entity.stopped_moving()
            
        if self.entity.playerNum == 1:
            # CHEATS: F1 F2 F3 F4 F5 F6 (Star, Shovel, Helmet, Grenade, StopWatch, Tank)
            if key == pygame.K_F1:
                self.entity.level.takeStarItem(self.entity, None)
            elif key == pygame.K_F2:
                self.entity.level.takeShovelItem(self.entity, None)
            elif key == pygame.K_F3:
                self.entity.level.takeHelmetItem(self.entity, None)
            elif key == pygame.K_F4:
                self.entity.level.takeGrenadeItem(self.entity, None)
            elif key == pygame.K_F5:
                self.entity.level.takeStopWatchItem(self.entity, None)
            elif key == pygame.K_F6:
                self.entity.level.takeTankItem(self.entity, None)
        elif self.entity.playerNum == 2:
            # CHEATS: F7 F8 F9 F10 F11 F12 (Star, Shovel, Helmet, Grenade, StopWatch, Tank)
            if key == pygame.K_F7:
                self.entity.level.takeStarItem(self.entity, None)
            elif key == pygame.K_F8:
                self.entity.level.takeShovelItem(self.entity, None)
            elif key == pygame.K_F9:
                self.entity.level.takeHelmetItem(self.entity, None)
            elif key == pygame.K_F10:
                self.entity.level.takeGrenadeItem(self.entity, None)
            elif key == pygame.K_F11:
                self.entity.level.takeStopWatchItem(self.entity, None)
            elif key == pygame.K_F12:
                self.entity.level.takeTankItem(self.entity, None)

    def mouse_key_down(self, event):
        pass

    def mouse_key_up(self, event):
        pass

    def mouse_move(self, event):
        pass

    def game_paused(self):
        # Stop moving if you were helding down movement keys
        self.downMoveKeys = []

    def freezePlayer(self):
        self.frozen = True
        self.freezeTicks = FREEZE_PENALTY_PERIOD
        self.freezeBlinkRate = FREEZE_BLINK_RATE
