## Project: Battle City Remake
## Author: Salwan Asaad
## Constructor Button

import pygame
import pyenkido.gui.button

class ConstructButton(pyenkido.gui.button.Button):
    def __init__(self, rect, image, is_toggle = False):
        super(ConstructButton, self).__init__(rect, is_toggle)
        self.image = image
        self.is_toggle = is_toggle
        self.w = self.rect.width
        self.h = self.rect.height
        ihw = self.image.get_width() / 2
        ihh = self.image.get_height() / 2
        self.x = self.rect.left + 2
        self.y = self.rect.top + 2
        cx = self.x + ((self.rect.width - 4) / 2)
        cy = self.y + ((self.rect.height - 4) / 2)
        self.ix = cx - ihw
        self.iy = cy - ihh
        self.xx = self.x + (self.rect.width - 4)
        self.yy = self.y + (self.rect.height - 4)

    def update(self):
        pass

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(self.x, self.y, self.w - 4, self.h - 4))
        screen.blit(self.image, (self.ix, self.iy))
        if self.state == pyenkido.gui.button.GUI_BUTTON_UP or self.state == pyenkido.gui.button.GUI_BUTTON_HOVER:
            pygame.draw.line(screen, (102, 102, 102), (self.xx, self.y), (self.xx, self.yy))
            pygame.draw.line(screen, (102, 102, 102), (self.x, self.yy), (self.xx, self.yy))
            pygame.draw.line(screen, (255, 255, 255), (self.x, self.y), (self.xx, self.y))
            pygame.draw.line(screen, (255, 255, 255), (self.x, self.y), (self.x, self.yy))
        else:
            pygame.draw.line(screen, (255, 255, 255), (self.xx, self.y), (self.xx, self.yy))
            pygame.draw.line(screen, (255, 255, 255), (self.x, self.yy), (self.xx, self.yy))
            pygame.draw.line(screen, (102, 102, 102), (self.x, self.y), (self.xx, self.y))
            pygame.draw.line(screen, (102, 102, 102), (self.x, self.y), (self.x, self.yy))