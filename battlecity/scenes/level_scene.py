## Project: BattleCity
## Module: Level Scene
## Author: Salwan

import pygame
import pyenkido.scene
import pyenkido.sound
import pyenkido.font
import battlecity.game_level
from battlecity.defs import *

class LevelScene(pyenkido.scene.Scene):
    def __init__(self, scene_mgr, screen):
        super(LevelScene, self).__init__(scene_mgr, screen)
        self.currentLevel = 1

    def start(self):
        self.bitmap = pyenkido.image_utils.load_image("res/textures", "sprites.png")
        # Build Enemy Textures
        self.enemyTextures = {}
        c = GAME_ENEMY_1_TANK
        for i in range(0, 4):
            t = c + i
            r = StripData[t]
            a1 = self.bitmap.subsurface(r)
            a2 = pygame.Surface((a1.get_width(), a1.get_height() * 4))
            a3 = None
            for j in range(0, 4):
                a3 = a1.copy()
                setTankPalette(a3, TANK_PAL_METAL + j)
                a2.blit(a3, (0, a1.get_height() * j))
            #pygame.image.save(a2, "enemy_texture" + str(i) + str(j) + ".png")
            a2.set_colorkey((255, 0, 255))
            self.enemyTextures[t] = a2        
        
        # Build Players Textures
        self.playerTextures = {}
        playerColor = {}
        playerColor[0] = TANK_PAL_ORANGE
        playerColor[1] = TANK_PAL_GREEN
        c = GAME_PLAYER_TANK_1
        for i in range(0, 2):
            color = playerColor[i]
            a2 = pygame.Surface((a1.get_width(), a1.get_height() * 4))
            for j in range(0, 4):
                t = c + j
                r = StripData[t]
                a1 = self.bitmap.subsurface(r).copy()
                setTankPalette(a1, color)
                a2.blit(a1, (0, a1.get_height() * j))
            a2.set_colorkey((255, 0, 255))
            #pygame.image.save(a2, "player" + str(i) + ".png")
            self.playerTextures[i + 1] = a2

        # Enable transperancy
        self.bitmap.set_colorkey((255, 0, 255))

        # Other stuff
        self.currentLevel = self.sceneMgr.gamedb["Level"]
        self.level = battlecity.game_level.GameLevel(self, self.screen, self.bitmap, self.currentLevel)
        self.font = pyenkido.font.Font()
        self.sceneMgr.gamedb["FragList"] = {}
        self.sceneMgr.gamedb["FragList"][1] = {}
        self.sceneMgr.gamedb["FragList"][2] = {}
        self.sceneMgr.gamedb["GameOver"] = False
        
        self.decoFlag = self.bitmap.subsurface(InterfaceData[INTERFACE_FLAG])
        self.decoEnemy = self.bitmap.subsurface(InterfaceData[INTERFACE_ENEMY])
        self.decoPlayer = self.bitmap.subsurface(InterfaceData[INTERFACE_PLAYER])       

        # Timing
        self.ticks = 0

        # God Mode Disabled by default
        self.level.godMode = False

        self.textPause = [(8,2),(21,3),(7,3),(4,3)]
        self.isPaused = False
        self.pauseBlinkState = True
        self.pauseTicks = 0
        self.pauseSound = pyenkido.sound.load_sound("res/sounds", "game_pause.ogg")
        self.pauseKeys = [pygame.K_ESCAPE]

        # Pause info
        self.pauseSurface = pygame.Surface((168, 48))
        self.pauseSurface.fill((0x33, 0x33, 0x33))
        pygame.draw.rect(self.pauseSurface, (0xff, 0xff, 0xff), pygame.Rect(0, 0, 168, 48), 1)
        (40, 156)
        self.font.ResetColorMask()
        self.font.DrawTextEn(self.pauseSurface, (4, 8), [(4,0),(18,0),(2,0),(0,0),(15,0),(4,0),(31,0)])
        self.font.DrawTextEn(self.pauseSurface, (4, 20), [(12, 0),(31,0)])
        self.font.DrawTextEn(self.pauseSurface, (4, 32), [(16, 0),(31,0)])
        continueText = [(0,2),(29,3),(22,2),(8,2),(13,3),(19,2),(0,2),(19,2),(0,5),(0,5),(0,5),(0,5),(0,5),(0,5),(0,5)]
        mmText = [(0,2),(11,3),(7,3),(1,2),(26,3),(13,3),(20,3),(0,5),(0,2),(11,3),(19,2),(26,3),(23,3),(22,2),(23,3),(20,3)]
        quitText = [(0,2),(11,3),(16,2),(19,2),(21,3),(11,2),(0,5),(13,3),(14,3),(0,5),(0,2),(11,3),(11,3),(34,2),(6,2),(20,3)]
        self.font.DrawTextArRL(self.pauseSurface, (60, 8), continueText)
        self.font.DrawTextArRL(self.pauseSurface, (53, 20), mmText)
        self.font.DrawTextArRL(self.pauseSurface, (53, 32), quitText)
        self.pausedSurfaceW = 0
    
    def update(self):
        self.ticks += 1        
        if not self.isPaused:
            self.updateControllers()
            self.level.update()
        self.updateParticles()
        
    def draw(self):
        self.screen.fill((127, 127, 127))
        self.level.draw()
        self.screen.blit(self.decoFlag, (232, 184))
        
        self.font.SetColorMask(0, 0, 0)
        self.drawLevelNumber()
        self.drawLivesCount()
        self.drawEnemyCount()
        self.drawParticles()

        if self.isPaused:
            w = self.pauseSurface.get_width()
            h = self.pauseSurface.get_height()
            hw = w / 2
            if self.pausedSurfaceW < hw:
                self.pausedSurfaceW += 5
            self.screen.blit(self.pauseSurface, (36 + (hw - self.pausedSurfaceW), 152),
                pygame.Rect((hw - self.pausedSurfaceW), 0, self.pausedSurfaceW * 2, h))

            self.pauseTicks += 1
            if self.pauseTicks > 20:
                self.pauseTicks = 0
                self.pauseBlinkState = not self.pauseBlinkState
            if self.pauseBlinkState:
                self.font.SetColorMask(0x60, 0xff, 0x71)
                self.font.DrawTextArRL(self.screen, (104,120), self.textPause)

    def drawLevelNumber(self):        
        if self.currentLevel < 10:
            self.font.DrawTextArRL(self.screen, (242, 200), [(self.currentLevel, 4)])
        else:
            tens = self.currentLevel / 10
            ones = self.currentLevel % 10
            self.font.DrawTextArRL(self.screen, (242, 200), [(ones, 4), (tens, 4)])

    def drawLivesCount(self):
        if 1 in self.level.playersAlive:
            self.screen.blit(self.decoPlayer, (233, 144))
            self.font.DrawTextASCII(self.screen, (233, 136), "IP")
            self.font.DrawTextArRL(self.screen, (241, 144), [(self.level.p1Lives, 4)])
        if 2 in self.level.playersAlive:
            self.screen.blit(self.decoPlayer, (233, 168))
            self.font.DrawTextEn(self.screen, (232, 160), [(24, 1), (15, 0)])
            self.font.DrawTextArRL(self.screen, (241, 168), [(self.level.p2Lives, 4)])

    def drawEnemyCount(self):
        for n in range(0, self.level.enemyCount):
            x = n % 2
            y = (n - x) / 2
            self.screen.blit(self.decoEnemy, (233 + (x * 8), 25 + (y * 8)))
        
    def key_down(self, key):
        pass
        
    def key_up(self, key):
        if key == pygame.K_g:
            self.level.godMode = not self.level.godMode
            if self.level.godMode:
                print "<<<< GOD MODE ENABLED >>>>"
            else:
                print "<<<< GOD MODE DISABLED >>>>"

        if key in self.pauseKeys:
            self.pauseGame()

        if self.isPaused:
            if key == pygame.K_m:
                # back to mainmenu
                self.sceneMgr.change_scene("GameMainMenu", False)
            elif key == pygame.K_q:
                # Quit
                self.sceneMgr.closeGame()
        
    def gameOver(self):
        print "<<<< GAME OVER >>>>"
        self.sceneMgr.gamedb["GameOver"] = True

    def pauseGame(self):
        if self.isPaused:
            self.resumeGame()
        else:
            self.pauseSound.play()
            self.isPaused = True
            self.pausedSurfaceW = 0
            for c in self.controllers:
                c.game_paused()
            self.level.game_paused()

    def resumeGame(self):
        if not self.isPaused:
            self.pauseGame()
        else:
            self.pauseSound.play()
            self.isPaused = False
            for c in self.controllers:
                c.game_resumed()
            self.level.game_resumed()

    def end(self):
        self.sceneMgr.gamedb["Lives"][1] = self.level.p1Lives
        self.sceneMgr.gamedb["Lives"][2] = self.level.p2Lives
        self.sceneMgr.stopAllSounds()
        self.sceneMgr.change_scene("LevelScore")
        
