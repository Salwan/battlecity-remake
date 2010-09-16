## Project: pyEnkido
## Module: GUI Control: Label
## Author: Salwan A. AlHelaly

import pyenkido.gui.control
from pyenkido.font import *

class Label(pyenkido.gui.control.Control):
    def __init__(self, at, text, color_mask = (1, 1, 1), b_ascii = True):
        super(Label, self).__init__()
        self.at = at
        self.rect = pygame.Rect(self.at[0], self.at[1], len(text) * 7, 8)
        self.text = text
        self.ascii = b_ascii
        self.font = Font()
        self.colorMask = color_mask

    def draw(self, screen):
        self.font.SetColorMask(self.colorMask[0], self.colorMask[1], self.colorMask[2])
        if self.ascii:
            self.font.DrawTextASCII(screen, self.at, self.text)
        else:
            self.font.DrawTextEn(screen, self.at, self.text)
        self.font.ResetColorMask()

