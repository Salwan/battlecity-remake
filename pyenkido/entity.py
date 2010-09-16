## Project: pyEnkido
## Module: entity
## Author: Salwan

import pygame

class Entity(pygame.sprite.Sprite):
    def __init__(self):
        super(Entity, self).__init__()
        self.controller = None
        self.type = -1
        self.alive = True
    
    def update(self):
        pass

    def preDraw(self, screen):
        pass

    def postDraw(self, screen):
        pass

    def setPosition(self, new_pos):
        self.rect = pygame.Rect(new_pos[0], new_pos[1], self.image.get_width(), self.image.get_height())

    def getPosition(self):
        return (self.rect.left, self.rect.top)

    def save(self, path, filename):
        pass

    def load(self, path, filename):
        pass

    def attached_to_controller(self, controller):
        self.controller = controller

    def detached_from_controller(self):
        self.controller = None

    def game_paused(self):
        pass

    def game_resumed(self):
        pass

    def spawned(self):
        pass

    def killed(self):
        pass

    def takeDamage(self, area = None, amount = 0):
        self.kill()

    def kill(self):
        self.killed()
        self.alive = False
        super(Entity, self).kill()

    def isAlive(self):
        return self.alive
        
