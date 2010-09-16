## Project: BattleCity
## Module: Level Score
## Author: Salwan

import pygame
import pyenkido.scene
import pyenkido.font
import pyenkido.screen_effects
from battlecity.defs import *

class LevelScoreScene(pyenkido.scene.Scene):
    def start(self):
        self.sprites = pyenkido.image_utils.load_image("res/textures", "sprites.png")
        self.sprites.set_colorkey((255, 0, 255))
        self.ticks = 0
        self.isCountingScore = False
        self.isDoneCounting = False
        self.showTotal = False
        
        self.font = pyenkido.font.Font()

        self.images = [
                        self.sprites.subsurface(GameData[GAME_ENEMY_1_TANK]),
                        self.sprites.subsurface(GameData[GAME_ENEMY_2_TANK]),
                        self.sprites.subsurface(GameData[GAME_ENEMY_3_TANK]),
                        self.sprites.subsurface(GameData[GAME_ENEMY_4_TANK])
                      ]
        for i in self.images:
            setTankPalette(i, TANK_PAL_METAL)

        self.textHiScore = [(2,2),(32,2),(11,3),(24,3),(0,5),(15,3),(7,3),(1,2),(29,2)]
        self.textRound = [(0,2),(11,3),(12,2),(21,3),(11,3),(20,3)]
        self.textPlayer1 = [(0,2),(11,3),(29,3),(32,2),(5,2),(0,5),(0,2),(30,3),(21,3),(10,3)]
        self.textPoints = [(15,3),(7,3),(29,2),(20,3),(0,5),(0,5),(0,5),(10,5)]
        self.textTotal = [(0,2),(11,3),(13,3),(12,2),(13,3),(21,3),(31,2)]
        self.scoreSound = pyenkido.sound.load_sound("res/sounds", "score_point.ogg")

        self.isCountingType = GAME_ENEMY_1_TANK
        self.scoreDetails = {GAME_ENEMY_1_TANK:None, GAME_ENEMY_2_TANK:None,
                             GAME_ENEMY_3_TANK:None, GAME_ENEMY_4_TANK:None}
        self.fragList = self.sceneMgr.gamedb["FragList"][1]
        self.enemyCount = 0
        for n in self.fragList.itervalues():
            self.enemyCount += n

        self.actionKeys = [pygame.K_SPACE, pygame.K_RETURN]
        self.accelerateCounting = False

    def update(self):
        self.ticks += 1
        if self.accelerateCounting and (not self.isCountingScore or not self.isDoneCounting):
            self.ticks += 5
        if not self.isCountingScore:
            if self.ticks > 60:
                self.isCountingScore = True
                self.ticks = 0
        elif not self.isDoneCounting:
            if self.ticks > 15:
                self.ticks = 0
                if self.scoreDetails[self.isCountingType] == None:
                    self.scoreDetails[self.isCountingType] = (0,0)
                else:
                    p = self.scoreDetails[self.isCountingType]
                    if self.isCountingType in self.fragList and p[0] < self.fragList[self.isCountingType]:
                        self.scoreDetails[self.isCountingType] = (p[0] + 1, p[1] + ScoreForEnemy[self.isCountingType])
                        self.scoreSound.play()
                    else:
                        self.isCountingType += 1
                        if self.isCountingType > GAME_ENEMY_4_TANK:
                            self.isDoneCounting = True
                            self.showTotal = True
        else:
            if self.ticks > 200:
                if self.sceneMgr.gamedb["GameOver"]:
                    self.sceneMgr.change_scene("GameOver")
                else:
                    print "WON!!! SHOULD START NEW ROUND..."
                    self.sceneMgr.add_screen_effect(pyenkido.screen_effects.SweepInEffect(self.screen, (0, 0, 0), False, True, False, 0, 15))
                    self.sceneMgr.gamedb["Level"] += 1
                    self.sceneMgr.change_scene("LevelDisplay")
                    #self.sceneMgr.closeGame()
                
    def draw(self):
        self.screen.fill((0, 0, 0))
        self.font.SetColorMask(0x50, 0xe0, 0x00)
        self.font.DrawTextArRL(self.screen, (128,24), self.textHiScore)       
        self.font.DrawTextArRL(self.screen, (152,56), self.textPlayer1)

        self.font.SetColorMask(0x00, 0xe0, 0x50)
        self.font.DrawNumberAr(self.screen, (48, 24), self.sceneMgr.gamedb["HiScore"], 7)
        self.font.DrawNumberAr(self.screen, (144,72),self.sceneMgr.gamedb["Score"][1], 7)

        self.font.ResetColorMask()
        self.font.DrawNumberAr(self.screen, (88, 40), self.sceneMgr.gamedb["Level"], 2)
        self.font.DrawTextArRL(self.screen, (120,40), self.textRound)

        for i in range(0, 4):
            self.font.DrawTextArRL(self.screen, (136,96 + (24 * i)), self.textPoints)
        self.font.DrawTextArRL(self.screen, (168,184), self.textTotal)
        pygame.draw.rect(self.screen, (255, 255, 255), pygame.Rect(96, 181, 65, 2))
        
        for i in range(0, 4):
            self.screen.blit(self.images[i], (121,92 + (24 * i)))

        i = 0
        for d in self.scoreDetails.itervalues():
            if d != None:
                # Tank Count
                self.font.DrawNumberAr(self.screen, (144,96 + (24 * i)), d[0])
                # Score
                self.font.DrawNumberAr(self.screen, (208,96 + (24 * i)), d[1])
            i+=1

        if self.showTotal:
            self.font.DrawNumberAr(self.screen, (144,184), self.enemyCount)

    def key_down(self, key):
        if key in self.actionKeys:
            self.accelerateCounting = True

    def key_up(self, key):
        if key in self.actionKeys and self.accelerateCounting:
            self.accelerateCounting = False




