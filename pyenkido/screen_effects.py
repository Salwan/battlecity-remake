## Project: pyEnkido
## Module: screen effects
## Author: Salwan

import pygame
import math_utils

class ScreenEffectBase:
    def __init__(self):
        pass
        
    def update(self):
        pass
        
    def draw(self, screen):
        pass
        
    def is_done(self):
        return self.isDone


class SlideInEffect(ScreenEffectBase):
    def __init__(self, screen, clear_color, startx, endx, starty, endy, delay, time, b_out = False):
        self.isDone = False
        self.startx = startx
        self.starty = starty
        self.endx = endx
        self.endy = endy
        self.delay = delay
        self.time = time
        self.tick = 0
        self.screen = screen
        self.clearColor = clear_color
        self.transitionScreen = self.screen.copy()
        self.out = b_out
        self.x = 0
        self.y = 0
        
    def update(self):
        if self.delay > 0:
            self.delay -= 1
        elif self.time > self.tick:
            self.tick += 1
            # calculate position
            delta = self.tick / float(self.time)
            if self.out:
                delta = 1.0 - delta
            self.x = math_utils.linear_interpolate(self.startx, self.endx, delta)
            self.y = math_utils.linear_interpolate(self.starty, self.endy, delta)
        else:
            self.isDone = True
        
    def draw(self, screen):
        self.transitionScreen.blit(self.screen, (0, 0))
        self.screen.fill(self.clearColor)
        self.screen.blit(self.transitionScreen, (self.x, self.y))
        
class SweepInEffect(ScreenEffectBase):
    def __init__(self, screen, clear_color, b_sweep_x, b_sweep_y, b_invert, delay, time, b_out = False):
        self.isDone = False
        self.delay = delay
        self.time = time
        self.tick = 0
        self.screen = screen
        self.clearColor = clear_color
        self.sweepX = b_sweep_x
        self.sweepY = b_sweep_y
        self.invert = b_invert
        self.out = b_out
        self.x = 0
        self.y = 0
        self.w = self.screen.get_width()
        self.h = self.screen.get_height()
        self.hw = self.w / 2
        self.hh = self.h / 2
        
    def update(self):
        if self.delay > 0:
            self.delay -= 1
        elif self.time > self.tick:
            self.tick += 1
            # calculate position
            delta = self.tick / float(self.time)
            if self.out:
                delta = 1.0 - delta
            self.x = math_utils.linear_interpolate(0, self.hw, delta)
            self.y = math_utils.linear_interpolate(0, self.hh, delta)
        else:
            self.isDone = True
        
    def draw(self, screen):
        if self.delay <= 0:
            if not self.invert:
                left = 0
                right = self.w
                top = 0
                bottom = self.h
                if self.sweepX:
                    left = self.x
                    right = self.w - self.x
                if self.sweepY:
                    top = self.y
                    bottom = self.h - self.y
                pygame.draw.rect(screen, self.clearColor, pygame.Rect(left, top, right - left, bottom - top))
            else:
                x1 = 0
                x2 = self.w
                y1 = 0
                y2 = self.h
                if self.sweepX:
                    x1 = (self.hw - self.x)
                    x2 = self.x + self.hw
                if self.sweepY:
                    y1 = (self.hh - self.y)
                    y2 = self.y + self.hh
                # x1
                pygame.draw.rect(screen, self.clearColor, pygame.Rect(0, 0, x1, self.h))
                # x2
                pygame.draw.rect(screen, self.clearColor, pygame.Rect(x2, 0, self.w - x2, self.h))
                # y1
                pygame.draw.rect(screen, self.clearColor, pygame.Rect(0, 0, self.w, y1))
                # y2
                pygame.draw.rect(screen, self.clearColor, pygame.Rect(0, y2, self.w, self.h - y2))
    
class ScreenEffectsManager:
    def __init__(self, screen):
        self.screen = screen
        self.effects = []
        
    def add_effect(self, effect):
        self.effects.append(effect)
    
    def update(self):
        effects_to_remove = []
        for efx in self.effects:
            if efx.is_done() == False:
                efx.update()
            else:
                effects_to_remove.append(efx)
        if len(effects_to_remove) > 0:
            for efx in effects_to_remove:
                self.effects.remove(efx)
        
    def draw(self):
        for efx in self.effects:
            efx.draw(self.screen)
            
    def clear(self):
        self.effects = []
    