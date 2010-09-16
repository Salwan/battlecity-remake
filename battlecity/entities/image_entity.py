## Project: pyEnkido
## Module: ImageEntity
## Author: Salwan

import os, pygame
import pyenkido.entity

class ImageEntity(pyenkido.entity.Entity):
    def __init__(self, image, position, type, layer = 0):
        super(ImageEntity, self).__init__()
        self.layer = layer
        self.type = type
        self.image = image
        self.rect = pygame.rect.Rect(position[0], position[1], self.image.get_width(), self.image.get_height())


class ImageEntityTimeKill(ImageEntity):
    def __init__(self, image, position, type, life_time, layer = 0):
        super(ImageEntityTimeKill, self).__init__(image, position, type, layer)
        self.life = life_time

    def update(self):
        self.life -= 1
        if self.life <= 0:
            self.kill()

    ### Hack to implement draw on top
    def postDraw(self, screen):
        if self.layer > 0:
            screen.blit(self.image, self.rect.topleft)
