## Project: BattleCity
## Module: New Hi Score
## Author: Salwan

import pygame
import pyenkido.scene
import pyenkido.font
import pyenkido.screen_effects
from battlecity.defs import *
import random

class NewHiScoreScene(pyenkido.scene.Scene):
    def start(self):
        self.sprites = pyenkido.image_utils.load_image("res/textures", "new_hiscore.png")
        self.font = pyenkido.font.Font()
        self.phrase = self.sprites.subsurface(pygame.Rect(10, 0, 221, 39))
        self.numberSprites = {}
        for i in range(0, 10):
            self.numberSprites[i] = self.sprites.subsurface(pygame.Rect(0 + (24 * i), 56, 24, 28))
        self.ticks = 0

        self.newHiScoreTone = pyenkido.sound.load_sound("res/sounds", "new_hiscore.ogg")
        self.newHiScoreTone.play()

        self.hiScore = self.sceneMgr.gamedb["HiScore"]
        self.hiScoreStr = str(self.hiScore)

    def update(self):
        self.ticks += 1
        if self.ticks > 60 * 9:
            self.sceneMgr.change_scene("GameMainMenu")


    def draw(self):
        self.screen.fill((0, 0, 0))
        r = random.randint(0x00, 0xff)
        g = random.randint(0x00, 0xff)
        b = random.randint(0x00, 0xff)
        self.phrase.set_masks((r, g, b, 0xff))
        self.screen.blit(self.phrase, (19, 49))

        # text
        self.font.DrawTextArRL(self.screen, (200, 30), [(13,3),(6,2),(19,2),(21,3),(8,3),(33,3)])

        # hi score
        x = 0
        for c in self.hiScoreStr:
            n = int(c)
            self.screen.blit(self.numberSprites[n], (x, 104))
            x += 24



