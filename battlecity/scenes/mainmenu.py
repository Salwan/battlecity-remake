## Project: BattleCity
## Module: Mainmenu
## Author: Salwan

import pygame
import pyenkido.scene
import pyenkido.font
import pyenkido.screen_effects
import battlecity.score_data
from battlecity.defs import *

class MainMenuScene(pyenkido.scene.Scene):
    def start(self):
        self.sceneMgr.add_screen_effect(pyenkido.screen_effects.SlideInEffect(self.screen, (0, 0, 0), 0, 0, self.screen.get_height(), 0, 0, 60 * 4))
        self.sprites = pyenkido.image_utils.load_image("res/textures", "sprites.png")
        self.sprites.set_colorkey((255, 0, 255))
        self.battleCityTitle = self.sprites.subsurface(pygame.Rect(0, 0, 188, 68))
        self.namcoLogo = self.sprites.subsurface(pygame.Rect(0, 70, 70, 8))
        self.ticks = 0
        self.font = pyenkido.font.Font()
        
        self.cursorActive = False
        self.cursorRate = 4
        self.cursorTick = 0
        self.cursorTank = [self.sprites.subsurface(MenuData[CURSOR_TANK_1]), self.sprites.subsurface(MenuData[CURSOR_TANK_2])]
        self.cursorState = 0
        self.cursorPosition = 0
        
        self.textP1Score = [(8,0),(11,1)]
        self.textP2Score = [(24,1), (11,1)]
        self.textHiScore = [(7,0),(8,0),(11,1)]
        self.text1Player = [(29,3),(32,2),(5,2),(0,5),(21,3),(0,2),(14,2),(17,2)]
        self.text2Player = [(29,3),(32,2),(6,2),(1,2),(14,3)]
        self.textCompany = [(1,1),(9,1),(8,1),(0,1),(0,5),(1,1),(9,1),(8,1),(5,1),(0,5),(13,0),(0,0),(12,0),(2,0),(14,0),(0,5),(11,0),(19,0),(3,0),(26,0)]
        self.textRemake = [(17,0),(4,0),(12,0),(0,0),(10,0),(4,0),(0,5),(1,0),(24,0),(0,5),(2,0),(11,0),(14,0),(20,0),(3,0),(12,0),(8,0),(11,0),(11,0),(0,5),(6,0),(0,0),(12,0),(4,0),(18,0)]
        self.textCopyrights = [(0,0),(11,0),(11,0),(0,5),(17,0),(8,0),(6,0),(7,0),(19,0),(18,0),(0,5),(17,0),(4,0),(18,0),(4,0),(17,0),(21,0),(4,0),(3,0)]
        self.textConstruct = [(13,3),(15,3),(7,3),(13,2),(0,5),(0,2),(11,3),(16,2),(19,2),(0,2),(26,3),(29,2)]
        self.textExit = [(0,2),(11,3),(16,2),(19,2),(21,3),(11,2)]

         # Load score info from score file
        scoreData = battlecity.score_data.ScoreData()
        scoreData = scoreData.load("game.bin")
        self.HiScore = scoreData.hiScore
        self.lastP1Score = scoreData.p1Score
        self.lastP2Score = scoreData.p2Score
        
    def update(self):
        self.ticks += 1
        if self.ticks > 60 * 4 and not self.cursorActive:
            self.cursorActive = True
        if self.cursorActive:
            self.cursorTick += 1
            if self.cursorTick >= self.cursorRate:
                self.cursorTick = 0
                self.cursorState = 1 - self.cursorState
        
    def draw(self):
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.battleCityTitle, (34, 48))
        pygame.draw.line(self.screen, (128, 128, 128), (0, 77), (self.screen.get_width(), 77))
        pygame.draw.line(self.screen, (128, 128, 128), (0, 86), (self.screen.get_width(), 86))
        self.screen.blit(self.namcoLogo, (88, 192))
        self.font.DrawTextEn(self.screen, (16,24), self.textP1Score)
        self.font.DrawTextEn(self.screen, (168, 24), self.textP2Score)
        self.font.DrawNumberAr(self.screen, (40,24), self.lastP1Score, 6)
        self.font.DrawNumberAr(self.screen, (192, 24), self.lastP2Score, 6)
        self.font.DrawTextEn(self.screen, (88,24), self.textHiScore)
        self.font.DrawNumberAr(self.screen, (108,24), self.HiScore, 6)
        self.font.DrawTextArRL(self.screen, (85,128), self.text1Player)
        self.font.DrawTextArRL(self.screen, (88,144), self.text2Player)
        self.font.DrawTextArRL(self.screen, (88,160), self.textConstruct)
        self.font.DrawTextArRL(self.screen, (88,176), self.textExit)
        
        self.font.DrawTextEn(self.screen, (28,208), self.textRemake)
        self.font.DrawCopyright(self.screen, (32, 224))
        self.font.DrawTextEn(self.screen, (48,224), self.textCompany)
        self.font.DrawTextEn(self.screen, (48,232), self.textCopyrights)
        
        if self.cursorActive:
            self.screen.blit(self.cursorTank[self.cursorState], (64, 124 + (self.cursorPosition * 16)))
            
    def select(self):       
        # Add information to game db after clearing it
        playerCount = 1
        if self.cursorPosition == 1:
            playerCount = 2
        self.sceneMgr.gamedb["PlayerCount"] = playerCount
        self.sceneMgr.gamedb["PlayersAlive"] = [1]
        if playerCount == 2:
            self.sceneMgr.gamedb["PlayersAlive"].append(2)
        self.sceneMgr.gamedb["TankLevel"] = {1:GAME_PLAYER_TANK_1, 2:GAME_PLAYER_TANK_1}
        self.sceneMgr.gamedb["LevelCount"] = 50
        self.sceneMgr.gamedb["Lives"] = {1:3, 2:3}
        self.sceneMgr.gamedb["Level"] = 1
        self.sceneMgr.gamedb["Score"] = {1:0, 2:0}
        self.sceneMgr.gamedb["HiScore"] = self.HiScore
        self.sceneMgr.add_screen_effect(pyenkido.screen_effects.SweepInEffect(self.screen, (0, 0, 0), False, True, False, 0, 15))
        
        if self.cursorPosition == 0:
            self.sceneMgr.change_scene("LevelDisplay")
        elif self.cursorPosition == 1:
            self.sceneMgr.change_scene("LevelDisplay")
        elif self.cursorPosition == 2:
            self.sceneMgr.change_scene("LevelEditor")
        else:
            self.sceneMgr.closeGame()
            
    def key_down(self, key):
        if key == pygame.K_DOWN and self.cursorActive:
            self.cursorPosition = self.cursorPosition + 1
            if self.cursorPosition > 3:
                self.cursorPosition = 3
        if key == pygame.K_UP and self.cursorActive:
            self.cursorPosition = self.cursorPosition - 1
            if self.cursorPosition < 0:
                self.cursorPosition = 0
        if key == pygame.K_SPACE or key == pygame.K_LCTRL or key == pygame.K_RETURN:
            if self.cursorActive:
                self.select()
            else:
                self.sceneMgr.clear_screen_effects()
                self.ticks = (60 * 4) + 1
        
