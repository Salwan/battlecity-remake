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
        self.sceneMgr.add_screen_effect(pyenkido.screen_effects.SlideInEffect(self.screen, (255, 255, 255), self.screen.get_width(), 0, 0, 0, 0, 60 *2))
        
    def update(self):
        self.ticks += 1
        if self.ticks > 60 * 3:
            self.sceneMgr.change_scene("GameMainMenu")
        
    def draw(self):
        if self.ticks < 60 * 2:
            self.screen.fill((0, 0, 0))
        else:
            self.screen.fill((0, 0, 0))
            
    def key_down(self, key):
        if key == pygame.K_SPACE or key == pygame.K_LCTRL or key == pygame.K_RETURN:
            self.sceneMgr.clear_screen_effects()
            self.ticks = 60 * 3
            