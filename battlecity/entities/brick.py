## Project: pyEnkido
## Module: Brick Tile
## Author: Salwan

import pygame
import pyenkido
from battlecity.defs import *
import battlecity.entities.tile

class Brick(battlecity.entities.tile.Tile):
    def __init__(self, group, bitmap, at, layer = 0):
        self.bitmap = bitmap
        super(Brick, self).__init__(group, bitmap.subsurface(TilesData[TILE_TYPE_BRICK]), pygame.Rect(0, 0, 16, 16), TILE_TYPE_BRICK, layer)
        self.image = self.image.copy()
        self.setPosition(at)
        pieces = [(0,0), (1,0), (0,1), (1,1)]
        self.rects = []
        for p in pieces:
            self.rects.append(pygame.rect.Rect(p[0] * 4, p[1] * 4, 4, 4))
        self.destroySound = pyenkido.sound.load_sound("res/sounds", "brick_destroy.ogg")

        # Determine if this is a base wall
        aat = (at[0] / 2, at[1] / 2)
        if aat in EAGLE_ADJ:
            self.eagleWall = True
        else:
            self.eagleWall = False


    def collideRect(self, rect):
        for r in self.rects:
            rc = pygame.rect.Rect(r.left + self.rect.left, r.top + self.rect.top, r.width, r.height)
            if rect.colliderect(rc):
                return True
        return False
    
    def takeDamage(self, area, amount = 0):
        to_remove = []
        for r in self.rects:
            rc = pygame.rect.Rect(r.left + self.rect.left, r.top + self.rect.top, r.width, r.height)
            if area.colliderect(rc):
                pygame.draw.rect(self.image, (0, 0, 0), r)
                to_remove.append(r)
        if len(to_remove) > 0:
            self.destroySound.play()
        for t in to_remove:
            self.rects.remove(t)
        if len(self.rects) <= 0:
            self.kill()

        #if self.eagleWall:
        #    print "YOU JUST HIT A FUCKING BASE WALL MADE OF BRICK!!!"

    def clearPieces(self, pieces_list):
        """pieces are in the form: [(0,0), (1,0), (0,1), (1,1)]"""
        rc = None
        for p in pieces_list:
            rc = pygame.rect.Rect(p[0] * 4, p[1] * 4, 4, 4)
            pygame.draw.rect(self.image, (0, 0, 0), rc)
            if rc in self.rects:
                self.rects.remove(rc)

    def isEagleWall(self):
        return self.eagleWall

    def getObjectCoords(self, pos):
        return ((pos[0] - 16) / 16, (pos[1] - 16) / 16)

