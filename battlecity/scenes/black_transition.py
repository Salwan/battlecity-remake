## Project: BattleCity
## Module: Introduction - black transition scene
## Author: Salwan

import pygame
import pyenkido.scene
import pyenkido.image_utils
import pyenkido.screen_effects

class IntroBlackTransitionScene(pyenkido.scene.Scene):
    def start(self):
        self.ticks = 0
        self.color = 255
        
    def update(self):
        self.ticks += 1
        if self.ticks > 60 * 3:
            self.sceneMgr.change_scene("GameMainMenu")
        self.color = pyenkido.math_utils.linear_interpolate(255, 0, self.ticks / (3.0 * 60.0))
        
    def draw(self):
        self.screen.fill((self.color, self.color, self.color))
            
    def key_down(self, key):
        if key == pygame.K_SPACE or key == pygame.K_LCTRL or key == pygame.K_RETURN:
            self.sceneMgr.clear_screen_effects()
            self.ticks = 60 * 3
            