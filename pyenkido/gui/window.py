## Project: pyEnkido
## Module: GUI Window control
## Author: Salwan A. AlHelaly

import pygame
import pyenkido.gui.control

class Window(object):
    def __init__(self, rect, title, b_has_close = False):
        self.rect = rect
        self.title = title
        self.has_close = b_has_close
        self.controls = {}
        self.guiMgr = None

    def update(self):
        for k, v in self.controls.iteritems():
            v.update()

    def draw(self, screen):
        for k, v in self.controls.iteritems():
            v.draw(screen)

    def lost_focus(self):
        for k, v in self.controls.iteritems():
            v.lost_focus()

    def gained_focus(self):
        for k, v in self.controls.iteritems():
            v.gained_focus()

    def mouse_over(self):
        pass

    def mouse_click(self):
        mouse_pos = pygame.mouse.get_pos()
        for k, v in self.controls.iteritems():
            if v.rect.collidepoint(mouse_pos):
                v.mouse_click()
                self.guiMgr.onClickEvent(k)

    def mouse_unclick(self):
        mouse_pos = pygame.mouse.get_pos()
        for k, v in self.controls.iteritems():
            if v.rect.collidepoint(mouse_pos):
                v.mouse_unclick()
                self.guiMgr.onUnclickEvent(k)

    def key_down(self, key):
        for k, v in self.controls.iteritems():
            v.key_down(key)

    def key_up(self, key):
        for k, v in self.controls.iteritems():
            v.key_up(key)

    def addControl(self, id, control):
        self.controls[id] = control

    def removeControl(self, id):
        del self.controls[id]

    def getControl(self, id):
        return self.controls[id]


class SimpleWindow(Window):
    def __init__(self, rect, title, b_has_close = False):
        super(SimpleWindow, self).__init__(rect, title, b_has_close)
        self.inRect = pygame.Rect(self.rect.left + 1, self.rect.top + 1, self.rect.width - 2, self.rect.height - 2)
        self.titleRect = pygame.Rect(self.rect.left, self.rect.top, self.rect.width, 12)
        self.font = pyenkido.font.Font()

    def draw(self, screen):
        pygame.draw.rect(screen, (204, 204, 204), self.rect)
        pygame.draw.rect(screen, (51, 51, 51), self.titleRect)
        pygame.draw.rect(screen, (0, 0, 255), self.rect, 1)
        pygame.draw.rect(screen, (102, 102, 102), self.inRect, 1)
        self.font.DrawTextASCII(screen, (self.rect.left + 3, self.rect.top + 3), self.title)
        super(SimpleWindow, self).draw(screen)

