## Project: BattleCity
## Module: Level Score
## Author: Salwan

import pygame
import pyenkido.scene
import pyenkido.font
import pyenkido.screen_effects
import battlecity.score_data
from battlecity.defs import *

class GameOverScene(pyenkido.scene.Scene):
    def start(self):
        self.sprites = pyenkido.image_utils.load_image("res/textures", "sprites.png")
        self.sprites.set_colorkey((255, 0, 255))
        self.ticks = 0
        self.gameOverImage = self.sprites.subsurface(GameData[GAME_OVER_BANNER])
        self.gameOverTone = pyenkido.sound.load_sound("res/sounds", "game_over.ogg")
        self.stage = 1
        self.newHiScore = False

        # Check for hiscore
        if self.sceneMgr.gamedb["Score"][1] > self.sceneMgr.gamedb["HiScore"]:
            # HI SCORE!!!!
            print "<<< HI-SCORE BROKEN BY PLAYER 1! >>>"
            self.sceneMgr.gamedb["HiScore"] = self.sceneMgr.gamedb["Score"][1]
            self.newHiScore = True
        if self.sceneMgr.gamedb["Score"][2] > self.sceneMgr.gamedb["HiScore"]:
            # HI SCORE!!!!
            print "<<< HI-SCORE BROKEN BY PLAYER 2! >>>"
            self.sceneMgr.gamedb["HiScore"] = self.sceneMgr.gamedb["Score"][2]
            self.newHiScore = True

        # Save new score
        scoreData = battlecity.score_data.ScoreData()
        scoreData.hiScore = self.sceneMgr.gamedb["HiScore"]
        scoreData.p1Score = self.sceneMgr.gamedb["Score"][1]
        if self.sceneMgr.gamedb["PlayerCount"] == 2:
            scoreData.p2Score = self.sceneMgr.gamedb["Score"][2]
        scoreData.save("game.bin")

    def update(self):
        self.ticks += 1
        if self.stage == 1:
            if self.ticks > 10:
                self.gameOverTone.play()
                self.stage += 1
                self.ticks = 0
        elif self.stage == 2:
            if self.ticks > 200:
                self.stage += 1
                self.ticks = 0
        elif self.stage == 3:
            if self.ticks > 10:
                if self.newHiScore:
                    self.sceneMgr.change_scene("NewHiScore")
                else:
                    self.sceneMgr.change_scene("GameMainMenu")


    def draw(self):
        self.screen.fill((0, 0, 0))
        if self.stage >= 2:
            self.screen.blit(self.gameOverImage, (62, 72))




