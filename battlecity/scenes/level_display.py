## Project: BattleCity
## Module: Level Display
## Author: Salwan

import pygame
import pyenkido.scene
import pyenkido.font
import pyenkido.image_utils
import pyenkido.screen_effects
import math

class LevelDisplay(pyenkido.scene.Scene):
    def start(self):
        self.ticks = 0
        self.font = pyenkido.font.Font()
        self.textLevel = [(0,2),(11,3),(12,2),(21,3),(11,3),(20,3),(0,5),(0,5),(0,5)]
        self.level = self.sceneMgr.gamedb["Level"]
        self.levelCount = self.sceneMgr.gamedb["LevelCount"]
        self.selected = False
        self.soundLevelStart = pyenkido.sound.load_sound("res/sounds", "level_start.ogg")
        if self.level > 1:
            self.returning = True
        else:
            self.returning = False
        
    def update(self):
        self.ticks += 1
        if not self.selected and self.returning and self.ticks > 60:
            self.select()
        if self.selected and self.ticks > 60:
            self.sceneMgr.add_screen_effect(pyenkido.screen_effects.SweepInEffect(self.screen, (128, 128, 128), False, True, True, 0, 15))
            self.sceneMgr.change_scene("LevelScene")
        
    def draw(self):
        self.screen.fill((128, 128, 128))
        self.font.SetColorMask(0, 0, 0)
        self.font.DrawTextArRL(self.screen, (96, 116), self.textLevel)
        ones = self.level % 10
        tens = math.floor(self.level / 10)
        text = []
        text.append((ones, 4))
        if tens > 0:
            text.append((tens, 4))
        else:
            text.append((0, 5))
        self.font.DrawTextArRL(self.screen, (96, 116), text)
        self.font.ResetColorMask()
        
    def select(self):
        self.selected = True
        self.ticks = 0
        self.sceneMgr.gamedb["Level"] = self.level
        self.sceneMgr.play_until_finish(self.soundLevelStart)
            
    def key_down(self, key):
        if not self.selected and not self.returning:
            if key == pygame.K_RIGHT:
                self.level += 1
                if self.level > self.levelCount:
                    self.level = 1
            if key == pygame.K_LEFT:
                self.level -= 1
                if self.level < 1:
                    self.level = self.levelCount
            if key == pygame.K_RETURN or key == pygame.K_SPACE or key == pygame.K_LCTRL:
                self.select()
        
