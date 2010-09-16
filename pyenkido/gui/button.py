## Project: pyEnkido
## Module: Button Control
## Author: Salwan A.AlHelaly

import pygame
import pyenkido.gui.control

# enum button states
GUI_BUTTON_UP = 0
GUI_BUTTON_HOVER = 1
GUI_BUTTON_DOWN = 2

class Button(pyenkido.gui.control.Control):
    def __init__(self, rect, is_toggle = False):
        super(Button, self).__init__()
        self.state = GUI_BUTTON_UP
        self.rect = rect
        self.is_toggle = is_toggle

    def update(self):
        pass

    def draw(self, screen):
        pass

    def mouse_over(self):
        self.state = GUI_BUTTON_HOVER

    def mouse_click(self):
        if not self.is_toggle:
            self.state = GUI_BUTTON_DOWN
        else:
            if self.state == GUI_BUTTON_DOWN:
                self.state = GUI_BUTTON_UP
            else:
                self.state = GUI_BUTTON_DOWN

    def mouse_unclick(self):
        if not self.is_toggle:
            self.state = GUI_BUTTON_UP

    def gained_focus(self):
        if not self.is_toggle:
            self.state = GUI_BUTTON_UP
