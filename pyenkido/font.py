# Project: pyEnkido
# Module: font
# Author: Salwan A. AlHelaly

import sys, pygame
import image_utils
from pyenkido.font_defs import *

class Font:
    def __init__(self):
        self.fontmap = image_utils.load_image("res/textures", "font.png")
        self.fontmap.set_colorkey((0, 0, 0))
        self.defaultMask = self.fontmap.get_masks()

    def DrawTextASCII(self, screen, at, text):
        try:
            cursor = 0
            for char in text:
                item = ASCII_MAP[char]
                screen.blit(self.fontmap, (at[0]+(cursor*8),at[1]), pygame.Rect(item[0] * 7, item[1] * 7, 7, 7))
                cursor += 1
        except e:
            raise e

    def DrawTextEn(self, screen, at, textlist):
        cursor = 0
        for item in textlist:
            screen.blit(self.fontmap, (at[0]+(cursor*8),at[1]), pygame.Rect(item[0] * 7, item[1] * 7, 7, 7))
            cursor += 1
            
    def DrawTextAr(self, screen, at, textlist):
        cursor = 0
        for item in textlist:
            screen.blit(self.fontmap, (at[0]+(cursor*7),at[1]), pygame.Rect(item[0] * 7, item[1] * 7, 7, 7))
            cursor += 1

    def DrawNumberAr(self, screen, at, number, places = 0):
        sn = str(number)
        textlist = []
        for c in sn:
            textlist.append((int(c), 4))
        if places > len(textlist):
            temp = []
            for i in range(0, places - len(textlist)):
                temp.append((0, 5))
            temp.extend(textlist)
            textlist = temp
        self.DrawTextAr(screen, at, textlist)
    
    # Draws arabic characters Right-to-Left
    # at: is still the left-top corner
    def DrawTextArRL(self, screen, at, textlist):
        cursor = len(textlist)-1
        for item in textlist:
            screen.blit(self.fontmap, (at[0]+(cursor*7),at[1]), pygame.Rect(item[0] * 7, item[1] * 7, 7, 7))
            cursor -= 1

    def DrawCopyright(self, screen, at):
        screen.blit(self.fontmap, at, pygame.Rect(237,0,8,8))
        
    def SetColorMask(self, b_red, b_green, b_blue):
        m = (self.defaultMask[0] * b_red, self.defaultMask[1] * b_green, self.defaultMask[2] * b_blue, 0)
        self.fontmap.set_masks(m)
        
    def ResetColorMask(self):
        self.fontmap.set_masks(self.defaultMask)
