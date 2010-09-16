## Project: pyEnkido
## Module: GUI Manager
## Author: Salwan A. AlHelaly

import pygame
from pyenkido.event import Event

class GUIManager:
    def __init__(self, screen):
        self.screen = screen
        self.windows = {}
        self.newWindows = []
        self.oldWindows = []
        self.mouse = None
        self.onClickEvent = Event()
        self.onUnclickEvent = Event()
        self.focusWindowID = None
        
    def update(self):
        if self.mouse:
            self.mouse.update()
        if self.focusWindowID in self.windows:
            self.windows[self.focusWindowID].update()
        self.flush()
        
    def draw(self):
        for k, v in self.windows.iteritems():
            v.draw(self.screen)
        if self.mouse:
            self.mouse.draw(self.screen)

    def setFocus(self, id):
        if self.focusWindowID in self.windows:
            self.windows[self.focusWindowID].lost_focus()
        self.focusWindowID = id
        self.windows[self.focusWindowID].gained_focus()

    def getActiveWindow(self):
        return self.windows[self.focusWindowID]

    def getActiveWindowID(self):
        return self.focusWindowID

    def isActiveWindow(self, id):
        if id == self.focusWindowID:
            return True
        else:
            return False

    def getWindowCount(self):
        return len(self.windows)

    def setMouseObject(self, mouse):
        self.mouse = mouse

    def getWindow(self, id):
        return self.windows[id]

    def flush(self):
        if len(self.oldWindows) > 0:
            for w in self.oldWindows:
                del self.windows[w]
                ws = self.windows.keys()
                self.setFocus(ws[-1])
        self.oldWindows = []
        if len(self.newWindows) > 0:
            for w in self.newWindows:
                self.windows[w[0]] = w[1]
                self.setFocus(w[0])
        self.newWindows = []

    def addWindow(self, id, window):
        window.guiMgr = self
        self.newWindows.append((id, window))

    def removeWindow(self, id):
        self.oldWindows.append(id)

    def key_down(self, key):
        if self.focusWindowID in self.windows:
            self.windows[self.focusWindowID].key_down(key)

    def key_up(self, key):
        if self.focusWindowID in self.windows:
            self.windows[self.focusWindowID].key_up(key)
        
    def mouse_key_down(self, event):
        if self.focusWindowID in self.windows:
            buttons = pygame.mouse.get_pressed()
            if self.mouse:
                self.mouse.mouse_key_down(event)
            if buttons[0]:
                mouse_pos = pygame.mouse.get_pos()
                if self.windows[self.focusWindowID].rect.collidepoint(mouse_pos):
                    self.windows[self.focusWindowID].mouse_click()

    def mouse_key_up(self, event):
        if self.focusWindowID in self.windows:
            buttons = pygame.mouse.get_pressed()
            if self.mouse:
                self.mouse.mouse_key_up(event)
            if not buttons[0]:
                mouse_pos = pygame.mouse.get_pos()
                if self.windows[self.focusWindowID].rect.collidepoint(mouse_pos):
                    self.windows[self.focusWindowID].mouse_unclick()
    
    def mouse_move(self, event):
        if self.mouse:
            self.mouse.mouse_move(event)
