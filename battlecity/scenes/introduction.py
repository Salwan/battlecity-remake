## Project: BattleCity
## Module: Introduction
## Author: Salwan

import pygame
import pyenkido.scene
import pyenkido.image_utils
import pyenkido.screen_effects

LOGO_VIEW_TIME = 10

class IntroScene(pyenkido.scene.Scene):
    def start(self):
        self.logoBg = pyenkido.image_utils.load_image("res/textures", "cloudmill_bg.png")
        self.logoFan = pyenkido.image_utils.load_image("res/textures", "cloudmill_fan.png")
        self.logoTitle = pyenkido.image_utils.load_image("res/textures", "cloudmill_title.png")
        self.cloud1 = pyenkido.image_utils.load_image("res/textures", "cloud1.png")
        self.cloud2 = pyenkido.image_utils.load_image("res/textures", "cloud2.png")
        self.logoFan.set_colorkey((255, 0, 255))
        self.logoTitle.set_colorkey((255, 0, 255))
        self.cloud1.set_colorkey((255, 0, 255))
        self.cloud2.set_colorkey((255, 0, 255))
        
        self.ticks = 0
        self.sceneMgr.add_screen_effect(pyenkido.screen_effects.SlideInEffect(self.screen, (255, 255, 255), 0, 0, self.screen.get_height(), 0, 0, 60 * 2))
        self.sceneMgr.add_screen_effect(pyenkido.screen_effects.SlideInEffect(self.screen, (255, 255, 255), 0, 0, 0, -self.screen.get_height(), 60 * (LOGO_VIEW_TIME - 2), 60 * 2))
        self.logoFanRoto = None
        self.angle = 0
        self.accum = 0.0
        self.offset = 0

        self.logoSound = pyenkido.sound.load_sound("res/sounds", "logo.ogg")
        self.logoSound.play()
        
    def update(self):
        self.ticks += 1
        if self.ticks > 60 * LOGO_VIEW_TIME:
            self.sceneMgr.change_scene("IntroBlackTransition")
        
    def draw(self):
        self.screen.fill((255, 255, 255))

        # Background
        self.screen.blit(self.logoBg, (0, 0))

        self.accum += 0.05
        if self.accum >= 1.0:
            self.accum = 0.0
            self.offset += 1

        # Clouds behind fan
        self.screen.blit(self.cloud1, (145 + self.offset, 47))
        self.screen.blit(self.cloud2, (52 + self.offset, 63))

        # Fan
        self.logoFanRoto = pygame.transform.rotate(self.logoFan, self.angle)
        self.angle -= 0.2
        fx = self.logoFanRoto.get_width() / 2
        fy = self.logoFanRoto.get_height() / 2
        self.screen.blit(self.logoFanRoto, (125 - fx, 110 - fy))
        
        # Clouds in front of fan
        self.screen.blit(self.cloud1, (46 + self.offset, 41))
        self.screen.blit(self.cloud2, (120 + self.offset, 85))

        # Title
        self.screen.blit(self.logoTitle, (6, 7))
        
    def key_down(self, key):
        if key == pygame.K_SPACE or key == pygame.K_LCTRL or key == pygame.K_RETURN:
            self.sceneMgr.clear_screen_effects()
            self.ticks = 60 * LOGO_VIEW_TIME + 1
            self.logoSound.stop()
        
