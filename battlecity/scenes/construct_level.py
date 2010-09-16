## Project: BattleCity
## Module: Construct Level Scene
## Author: Salwan

import pygame, math
import pyenkido.scene
import pyenkido.image_utils
from pyenkido.gui import *
from battlecity.gui import *

# Dealing with py2exe bug
import pyenkido.gui.button
import pyenkido.gui.control
import pyenkido.gui.gui_manager
import pyenkido.gui.label
import pyenkido.gui.window
import battlecity.gui.construct_button

import battlecity.level
import battlecity.entities.brick
import battlecity.entities.water
import battlecity.entities.stone
import battlecity.entities.ice
import battlecity.entities.tree
import battlecity.gui.level_label
from battlecity.defs import *

# enum ControlIDS
BUTTON_ID_GRID = 0
BUTTON_ID_BRICK = 1
BUTTON_ID_STONE = 2
BUTTON_ID_TREE = 3
BUTTON_ID_WATER = 4
BUTTON_ID_ICE = 5
BUTTON_ID_ERASE = 6
BUTTON_ID_NEW = 7
BUTTON_ID_LOAD = 8
BUTTON_ID_SAVE = 9
BUTTON_ID_EXIT = 10
BUTTON_ID_1x = 11
BUTTON_ID_4x = 12

class ConstructMouse:
    def __init__(self, construct_level, bitmap):
        self.constructor = construct_level
        self.bitmap = bitmap
        self.cursors = {BUTTON_ID_ERASE:self.bitmap.subsurface(pygame.Rect(64, 240, 9, 13)),
                        BUTTON_ID_BRICK:self.bitmap.subsurface(pygame.Rect(74, 240, 9, 13)),
                        BUTTON_ID_STONE:self.bitmap.subsurface(pygame.Rect(84, 240, 9, 13)),
                        BUTTON_ID_TREE:self.bitmap.subsurface(pygame.Rect(94, 240, 9, 13)),
                        BUTTON_ID_WATER:self.bitmap.subsurface(pygame.Rect(104, 240, 9, 13)),
                        BUTTON_ID_ICE:self.bitmap.subsurface(pygame.Rect(114, 240, 9, 13))}
        self.currentCursor = BUTTON_ID_ERASE
        self.x = 128
        self.y = 120
        
    def setCursor(self, type):
        print "> ConstructMouse cursor is set to ", type
        self.currentCursor = type
        
    def update(self):
        pass
        
    def draw(self, screen):
        screen.blit(self.cursors[self.currentCursor], (self.x, self.y))
        
    def getPosition(self):
        return (self.x, self.y)
        
    def mouse_move(self, event):
        p = pygame.mouse.get_pos()
        self.x = p[0]
        self.y = p[1]
        if self.x < 0: self.x = 0
        if self.x > 255: self.x = 255
        if self.y < 0: self.y = 0
        if self.y > 239: self.y = 239

    def mouse_key_down(self, event):
        pass

    def mouse_key_up(self, event):
        pass

class ConstructLevel(pyenkido.scene.Scene):
    def start(self):
        self.bitmap = pyenkido.image_utils.load_image("res/textures", "sprites.png")
        self.bitmap.set_colorkey((255, 0, 255))
        self.level = battlecity.level.Level(self.screen, self.bitmap)
        self.mouse = ConstructMouse(self, self.bitmap)
        self.guiMgr.setMouseObject(self.mouse)
        self.gridArea = pygame.Rect(16, 16, 208, 208)
        self.displayGrid = True
        self.prevCursor = BUTTON_ID_BRICK

        self.font = pyenkido.font.Font()
        self.textConstruct = [(13,3),(15,3),(7,3),(13,2),(0,5),(0,2),(11,3),(16,2),(19,2),(0,2),(26,3),(29,2)]

        # Window for controls
        self.guiMgr.addWindow(WINDOW_CONSTRUCT, window.Window(self.screen.get_rect(), "Construct Level"))
        self.guiMgr.flush()

        # Grid Button
        self.guiMgr.getWindow(WINDOW_CONSTRUCT).addControl(BUTTON_ID_GRID, battlecity.gui.construct_button.ConstructButton(pygame.Rect(16, 224, 32, 16), self.bitmap.subsurface(36, 248, 18, 7), True))
        self.guiMgr.getWindow(WINDOW_CONSTRUCT).addControl(BUTTON_ID_BRICK, battlecity.gui.construct_button.ConstructButton(pygame.Rect(224, 16, 16, 16), self.bitmap.subsurface(8, 96, 8, 8), False))
        self.guiMgr.getWindow(WINDOW_CONSTRUCT).addControl(BUTTON_ID_STONE, battlecity.gui.construct_button.ConstructButton(pygame.Rect(240, 16, 16, 16), self.bitmap.subsurface(16, 96, 8, 8), False))
        self.guiMgr.getWindow(WINDOW_CONSTRUCT).addControl(BUTTON_ID_WATER, battlecity.gui.construct_button.ConstructButton(pygame.Rect(224, 32, 16, 16), self.bitmap.subsurface(0, 104, 8, 8), False))
        self.guiMgr.getWindow(WINDOW_CONSTRUCT).addControl(BUTTON_ID_TREE, battlecity.gui.construct_button.ConstructButton(pygame.Rect(240, 32, 16, 16), self.bitmap.subsurface(24, 96, 8, 8), False))
        self.guiMgr.getWindow(WINDOW_CONSTRUCT).addControl(BUTTON_ID_ICE, battlecity.gui.construct_button.ConstructButton(pygame.Rect(224, 48, 16, 16), self.bitmap.subsurface(32, 96, 8, 8), False))
        self.guiMgr.getWindow(WINDOW_CONSTRUCT).addControl(BUTTON_ID_ERASE, battlecity.gui.construct_button.ConstructButton(pygame.Rect(224, 64, 32, 16), self.bitmap.subsurface(0, 240, 19, 7), False))
        self.guiMgr.getWindow(WINDOW_CONSTRUCT).addControl(BUTTON_ID_NEW, battlecity.gui.construct_button.ConstructButton(pygame.Rect(224, 176, 32, 16), self.bitmap.subsurface(0, 248, 15, 7), False))
        self.guiMgr.getWindow(WINDOW_CONSTRUCT).addControl(BUTTON_ID_LOAD, battlecity.gui.construct_button.ConstructButton(pygame.Rect(224, 192, 32, 16), self.bitmap.subsurface(20, 240, 19, 7), False))
        self.guiMgr.getWindow(WINDOW_CONSTRUCT).addControl(BUTTON_ID_SAVE, battlecity.gui.construct_button.ConstructButton(pygame.Rect(224, 208, 32, 16), self.bitmap.subsurface(16, 248, 19, 7), False))
        self.guiMgr.getWindow(WINDOW_CONSTRUCT).addControl(BUTTON_ID_EXIT, battlecity.gui.construct_button.ConstructButton(pygame.Rect(224, 224, 32, 16), self.bitmap.subsurface(40, 240, 15, 7), False))
        self.guiMgr.getWindow(WINDOW_CONSTRUCT).addControl(BUTTON_ID_1x, battlecity.gui.construct_button.ConstructButton(pygame.Rect(224, 96, 32, 16), self.bitmap.subsurface(128, 248, 22, 8), True))
        self.guiMgr.getWindow(WINDOW_CONSTRUCT).addControl(BUTTON_ID_4x, battlecity.gui.construct_button.ConstructButton(pygame.Rect(224, 112, 32, 16), self.bitmap.subsurface(160, 248, 23, 8), True))
        self.guiMgr.getWindow(WINDOW_CONSTRUCT).getControl(BUTTON_ID_GRID).state = pyenkido.gui.button.GUI_BUTTON_DOWN
        self.guiMgr.getWindow(WINDOW_CONSTRUCT).getControl(BUTTON_ID_1x).state = pyenkido.gui.button.GUI_BUTTON_DOWN

        # Listen on gui events
        self.guiMgr.onClickEvent += self.handleOnClick
        
        self.shouldExit = False
        self.mouseDown = False
        self.ticks = 0

    def handleOnClick(self, id):
        if id == BUTTON_ID_GRID:
            if self.guiMgr.getWindow(WINDOW_CONSTRUCT).getControl(id).state == pyenkido.gui.button.GUI_BUTTON_DOWN:
                self.displayGrid = True
            else:
                self.displayGrid = False
        elif id == BUTTON_ID_BRICK:
            self.mouse.currentCursor = BUTTON_ID_BRICK
            self.prevCursor = BUTTON_ID_BRICK
        elif id == BUTTON_ID_STONE:
            self.mouse.currentCursor = BUTTON_ID_STONE
            self.prevCursor = BUTTON_ID_STONE
        elif id == BUTTON_ID_WATER:
            self.mouse.currentCursor = BUTTON_ID_WATER
            self.prevCursor = BUTTON_ID_WATER
        elif id == BUTTON_ID_TREE:
            self.mouse.currentCursor = BUTTON_ID_TREE
            self.prevCursor = BUTTON_ID_TREE
        elif id == BUTTON_ID_ICE:
            self.mouse.currentCursor = BUTTON_ID_ICE
            self.prevCursor = BUTTON_ID_ICE
        elif id == BUTTON_ID_ERASE:
            self.mouse.currentCursor = BUTTON_ID_ERASE
        elif id == BUTTON_ID_NEW:
            self.level = battlecity.level.Level(self.screen, self.bitmap)
        elif id == BUTTON_ID_SAVE:
            self.doSave()
        elif id == BUTTON_ID_LOAD:
            self.doLoad()
        elif id == BUTTON_ID_EXIT:
            self.setExit()
        elif id == BUTTON_YES:
            if self.guiMgr.getActiveWindowID() == WINDOW_LOAD_LEVEL:
                print "<loading level: %s.map>" % ((self.guiMgr.getActiveWindow().getControl(TEXT_LEVEL_NUMBER).level))
                self.level.load("res/maps", "%s.map" % (self.guiMgr.getActiveWindow().getControl(TEXT_LEVEL_NUMBER).level))
                self.guiMgr.removeWindow(WINDOW_LOAD_LEVEL)
            elif self.guiMgr.getActiveWindowID() == WINDOW_SAVE_LEVEL:
                print "<saving level: %s.map>" % ((self.guiMgr.getActiveWindow().getControl(TEXT_LEVEL_NUMBER).level))
                self.level.save("res/maps", "%s.map" % (self.guiMgr.getActiveWindow().getControl(TEXT_LEVEL_NUMBER).level))
                self.guiMgr.removeWindow(WINDOW_SAVE_LEVEL)
        elif id == BUTTON_NO:
            if self.guiMgr.getActiveWindowID() == WINDOW_LOAD_LEVEL:
                self.guiMgr.removeWindow(WINDOW_LOAD_LEVEL)
            elif self.guiMgr.getActiveWindowID() == WINDOW_SAVE_LEVEL:
                self.guiMgr.removeWindow(WINDOW_SAVE_LEVEL)
        elif id == BUTTON_ID_1x:
            self.guiMgr.getWindow(WINDOW_CONSTRUCT).getControl(BUTTON_ID_1x).state = pyenkido.gui.button.GUI_BUTTON_DOWN
            self.guiMgr.getWindow(WINDOW_CONSTRUCT).getControl(BUTTON_ID_4x).state = pyenkido.gui.button.GUI_BUTTON_UP
        elif id == BUTTON_ID_4x:
            self.guiMgr.getWindow(WINDOW_CONSTRUCT).getControl(BUTTON_ID_1x).state = pyenkido.gui.button.GUI_BUTTON_UP
            self.guiMgr.getWindow(WINDOW_CONSTRUCT).getControl(BUTTON_ID_4x).state = pyenkido.gui.button.GUI_BUTTON_DOWN

    def update(self):
        if not self.shouldExit:
            self.level.update()
            self.checkForMouseHold()
        elif self.ticks > 30:
            self.sceneMgr.change_scene("GameMainMenu")
        else:
            self.ticks += 1
        
    def draw(self):
        self.screen.fill((128, 128, 128))
        self.font.DrawTextArRL(self.screen, (88, 4), self.textConstruct)
        self.level.draw()
        if self.displayGrid:
            # Drawing a grid
            for i in range(16, 225, 16):
                pygame.draw.line(self.screen, (48, 48, 48), (16, i), (224, i))
                pygame.draw.line(self.screen, (48, 48, 48), (i, 16), (i, 224))

    def setExit(self):
        self.sceneMgr.add_screen_effect(pyenkido.screen_effects.SweepInEffect(self.screen, (0, 0, 0), False, True, True, 0, 30, True))
        self.shouldExit = True

    def doSave(self):
        #self.level.save("res/maps", "test.map")
        win = window.SimpleWindow(pygame.Rect(32, 48, 176, 96), "SAVE: CHOOSE LEVEL")
        win.addControl(TEXT_LEVEL_NUMBER, battlecity.gui.level_label.LevelLabel((110, 80), 1, (0, 0, 0)))
        win.addControl(TEXT_LEVEL_NUMBER_LEFT, label.Label((70, 80), "<", (0, 0, 0)))
        win.addControl(TEXT_LEVEL_NUMBER_RIGHT, label.Label((150, 80), ">", (0, 0, 0)))
        win.addControl(BUTTON_YES, battlecity.gui.construct_button.ConstructButton(pygame.Rect(48, 114, 48, 16), self.bitmap.subsurface(128, 240, 15, 7), False))
        win.addControl(BUTTON_NO, battlecity.gui.construct_button.ConstructButton(pygame.Rect(140, 114, 48, 16), self.bitmap.subsurface(144, 240, 11, 7), False))
        self.guiMgr.addWindow(WINDOW_SAVE_LEVEL, win)

    def doLoad(self):
        #self.level.load("res/maps", "test.map")
        win = window.SimpleWindow(pygame.Rect(32, 48, 176, 96), "LOAD: CHOOSE LEVEL")
        win.addControl(TEXT_LEVEL_NUMBER, battlecity.gui.level_label.LevelLabel((110, 80), 1, (0, 0, 0)))
        win.addControl(TEXT_LEVEL_NUMBER_LEFT, label.Label((70, 80), "<", (0, 0, 0)))
        win.addControl(TEXT_LEVEL_NUMBER_RIGHT, label.Label((150, 80), ">", (0, 0, 0)))
        win.addControl(BUTTON_YES, battlecity.gui.construct_button.ConstructButton(pygame.Rect(48, 114, 48, 16), self.bitmap.subsurface(128, 240, 15, 7), False))
        win.addControl(BUTTON_NO, battlecity.gui.construct_button.ConstructButton(pygame.Rect(140, 114, 48, 16), self.bitmap.subsurface(144, 240, 11, 7), False))
        self.guiMgr.addWindow(WINDOW_LOAD_LEVEL, win)

    def brush1xTo4x(self, at):
        att = [(at[0] * 2, at[1] * 2),
            (1 + at[0] * 2, at[1] * 2),
            (at[0] * 2, 1 + at[1] * 2),
            (1 + at[0] * 2, 1 + at[1] * 2)]
        return att

    def placeBrick(self, at):
        self.level.map.clearTile(at)
        self.level.map.createTile(at, TILE_TYPE_BRICK)

    def placeBrick4(self, at):
        for p in self.brush1xTo4x(at):
            self.placeBrick(p)

    def placeWater(self, at):
        self.level.map.clearTile(at)
        self.level.map.createTile(at, TILE_TYPE_WATER)

    def placeWater4(self, at):
        for p in self.brush1xTo4x(at):
            self.placeWater(p)

    def placeStone(self, at):
        self.level.map.clearTile(at)
        self.level.map.createTile(at, TILE_TYPE_STONE)

    def placeStone4(self, at):
        for p in self.brush1xTo4x(at):
            self.placeStone(p)

    def placeIce(self, at):
        self.level.map.clearTile(at)
        self.level.map.createTile(at, TILE_TYPE_ICE)

    def placeIce4(self, at):
        for p in self.brush1xTo4x(at):
            self.placeIce(p)

    def placeTree(self, at):
        self.level.map.clearTile(at)
        self.level.map.createTile(at, TILE_TYPE_TREE)

    def placeTree4(self, at):
        for p in self.brush1xTo4x(at):
            self.placeTree(p)

    def checkForMouseHold(self):
        if self.shouldExit:
            return
        if self.mouseDown:
            buttons = pygame.mouse.get_pressed()
            pos = self.mouse.getPosition()
            # Draw everywhere
            self.mouseClick(buttons, pos)
        
    def mouseClick(self, buttons, pos):
        if self.shouldExit:
            return
        # Left click
        if buttons[0]:
            if self.gridArea.collidepoint(pos) and self.guiMgr.isActiveWindow(WINDOW_CONSTRUCT):
                tile_pos_16 = self.level.map.getObjectCoords(pos)
                tile_pos_8 = self.level.map.getTileCoords(pos)
                if self.level.map.getObjectType(tile_pos_16) != TILE_TYPE_EAGLE:
                    if self.guiMgr.getActiveWindow().getControl(BUTTON_ID_1x).state == pyenkido.gui.button.GUI_BUTTON_DOWN:
                        if self.mouse.currentCursor == BUTTON_ID_BRICK:
                            self.placeBrick(tile_pos_8)
                        elif self.mouse.currentCursor == BUTTON_ID_WATER:
                            self.placeWater(tile_pos_8)
                        elif self.mouse.currentCursor == BUTTON_ID_STONE:
                            self.placeStone(tile_pos_8)
                        elif self.mouse.currentCursor == BUTTON_ID_ICE:
                            self.placeIce(tile_pos_8)
                        elif self.mouse.currentCursor == BUTTON_ID_TREE:
                            self.placeTree(tile_pos_8)
                        elif self.mouse.currentCursor == BUTTON_ID_ERASE:
                            self.level.map.clearTile(tile_pos_8)
                            self.level.map.clearObject(tile_pos_16)
                    else:
                        if self.mouse.currentCursor == BUTTON_ID_BRICK:
                            self.placeBrick4(tile_pos_16)
                        elif self.mouse.currentCursor == BUTTON_ID_WATER:
                            self.placeWater4(tile_pos_16)
                        elif self.mouse.currentCursor == BUTTON_ID_STONE:
                            self.placeStone4(tile_pos_16)
                        elif self.mouse.currentCursor == BUTTON_ID_ICE:
                            self.placeIce4(tile_pos_16)
                        elif self.mouse.currentCursor == BUTTON_ID_TREE:
                            self.placeTree4(tile_pos_16)
                        elif self.mouse.currentCursor == BUTTON_ID_ERASE:
                            for p in self.brush1xTo4x(tile_pos_16):
                                self.level.map.clearTile(p)
                            self.level.map.clearObject(tile_pos_16)

    def mouseUnclick(self, buttons, pos):
        pass
        
    def key_down(self, key):
        if self.shouldExit:
            return
        if key == pygame.K_g:
            self.displayGrid = 1 - self.displayGrid
            if self.displayGrid:
                self.guiMgr.getWindow(WINDOW_CONSTRUCT).getControl(BUTTON_ID_GRID).state = pyenkido.gui.button.GUI_BUTTON_DOWN
            else:
                self.guiMgr.getWindow(WINDOW_CONSTRUCT).getControl(BUTTON_ID_GRID).state = pyenkido.gui.button.GUI_BUTTON_UP
        elif key == pygame.K_e:
            if self.mouse.currentCursor != BUTTON_ID_ERASE:
                self.mouse.currentCursor = BUTTON_ID_ERASE
            else:
                self.mouse.currentCursor = self.prevCursor
        elif key == pygame.K_n:
            if self.guiMgr.getActiveWindowID() == WINDOW_CONSTRUCT:
                self.handleOnClick(BUTTON_ID_NEW)
        elif key == pygame.K_s:
            if self.guiMgr.getActiveWindowID() == WINDOW_CONSTRUCT:
                self.handleOnClick(BUTTON_ID_SAVE)
        elif key == pygame.K_l:
            if self.guiMgr.getActiveWindowID() == WINDOW_CONSTRUCT:
                self.handleOnClick(BUTTON_ID_LOAD)
        elif key == pygame.K_x:
            if self.guiMgr.getActiveWindowID() == WINDOW_CONSTRUCT:
                self.handleOnClick(BUTTON_ID_EXIT)
        elif key == pygame.K_F1:
            if self.guiMgr.getActiveWindowID() == WINDOW_CONSTRUCT:
                self.handleOnClick(BUTTON_ID_BRICK)
        elif key == pygame.K_F2:
            if self.guiMgr.getActiveWindowID() == WINDOW_CONSTRUCT:
                self.handleOnClick(BUTTON_ID_STONE)
        elif key == pygame.K_F3:
            if self.guiMgr.getActiveWindowID() == WINDOW_CONSTRUCT:
                self.handleOnClick(BUTTON_ID_WATER)
        elif key == pygame.K_F4:
            if self.guiMgr.getActiveWindowID() == WINDOW_CONSTRUCT:
                self.handleOnClick(BUTTON_ID_TREE)
        elif key == pygame.K_F5:
            if self.guiMgr.getActiveWindowID() == WINDOW_CONSTRUCT:
                self.handleOnClick(BUTTON_ID_ICE)
        elif key == pygame.K_n:
            if self.guiMgr.getActiveWindowID() == WINDOW_LOAD_LEVEL or self.guiMgr.getActiveWindowID() == WINDOW_SAVE_LEVEL:
                self.handleOnClick(BUTTON_NO)
        elif key == pygame.K_y:
            if self.guiMgr.getActiveWindowID() == WINDOW_LOAD_LEVEL or self.guiMgr.getActiveWindowID() == WINDOW_SAVE_LEVEL:
                self.handleOnClick(BUTTON_YES)
        elif key == pygame.K_1:
            if self.guiMgr.getActiveWindowID() == WINDOW_CONSTRUCT:
                self.handleOnClick(BUTTON_ID_1x)
        elif key == pygame.K_4:
            if self.guiMgr.getActiveWindowID() == WINDOW_CONSTRUCT:
                self.handleOnClick(BUTTON_ID_4x)
        
    def key_up(self, key):
        pass
        
    def mouse_key_down(self, event):
        if self.shouldExit:
            return
        buttons = pygame.mouse.get_pressed()
        pos = self.mouse.getPosition() 
        self.mouseClick(buttons, pos)
        self.mouseDown = True
        
    def mouse_key_up(self, event):
        self.mouseDown = False
        if self.shouldExit:
            return
        buttons = pygame.mouse.get_pressed()
        pos = self.mouse.getPosition()
        self.mouseUnclick(buttons, pos)
        
    def mouse_move(self, event):
        pass
        
    def end(self):
        pass
        
