## Project: pyEnkido
## Module: game
## Author: Salwan


import sys, pygame
import scene_manager
import screen_effects
from preferences import *


def BoolToString(value):
    if value:
        return "True"
    else:
        return "False"
        
##class GameInfo:
##    def __init__(self, game_preferences, scene_manager, screen):
##        self.gamePreferences = game_preferences
##        self.sceneMgr = scene_manager
##        self.screen = screen

class Game:
    def __init__(self, preferences):
        self.fullscreen = preferences.fullscreen
        self.renderingResolution = preferences.renderingResolution
        self.displayResolution = preferences.displayResolution
        self.scaleFilter = preferences.scaleFilter

        if preferences.iconFile != "":
            pygame.display.set_icon(pygame.image.load(preferences.iconFile))
        
        # initialize pygame
        pygame.init()
        if self.fullscreen == True:
            self.backbuffer = pygame.display.set_mode(self.displayResolution, pygame.DOUBLEBUF|pygame.HWSURFACE|pygame.FULLSCREEN)
            self.size = self.displayResolution
        else:
            self.backbuffer = pygame.display.set_mode(self.displayResolution, pygame.DOUBLEBUF|pygame.HWSURFACE)
            self.size = self.displayResolution;
            
        # initialize mouse
        pygame.mouse.set_visible(preferences.mouseVisible)
        
        # initialize screen
        if preferences.alpha:
            self.screen = pygame.surface.Surface(self.renderingResolution, pygame.SRCALPHA)
            self.screen = self.screen.convert_alpha()
        else:
            self.screen = pygame.surface.Surface(self.renderingResolution)
        self.screen.fill((0, 0, 0, 255))
        
        # initialize screen effects
        self.screenEffectsMgr = screen_effects.ScreenEffectsManager(self.screen)
        
        # initialize clock
        self.framerate = preferences.framerate
        self.framePeriod = 1.0 / float(self.framerate)
        self.clock = pygame.time.Clock()
        self.prevTime = 0.0
        self.curTime = 0.0
        self.frameTimeMS = 0.0
        self.frameTimeS = 0.0
        
        # initialize game
        self.gameTitle = preferences.gameTitle
        self.requestQuit = False
        self.sceneMgr = scene_manager.SceneManager(self.screen, self.screenEffectsMgr)
        ##self.gameInfo = GameInfo(preferences, self.sceneMgr, self.screen)
        
        # Display device info
        print "Display Device Information"
        print "==========================\n"
        videoInfo = pygame.display.Info()
        print "Hardware accelerated: ", BoolToString(videoInfo.hw)
        print "Video memory: ", videoInfo.video_mem
        print "Bits per pixel: ", videoInfo.bitsize
        print "Hardware surface blitting: ", BoolToString(videoInfo.blit_hw)
        print "Hardware surface color-key blitting: ", BoolToString(videoInfo.blit_hw_CC)
        print "Hardware surface alpha blitting: ", BoolToString(videoInfo.blit_hw_A)
        print "Software surface blitting: ", BoolToString(videoInfo.blit_sw)
        print "Software surface color-key blitting: ", BoolToString(videoInfo.blit_sw_CC)
        print "Software surface alpha blitting: ", BoolToString(videoInfo.blit_sw_A)
        print "Current display mode: ", videoInfo.current_w, "x", videoInfo.current_h
        
        # Audio info
        pygame.mixer.init(buffer=512)
        print "\n\nAudio Device Information"
        print "========================\n"
        audio_info = pygame.mixer.get_init()
        print "Audio Mixer available: ", BoolToString(len(audio_info))
        if len(audio_info):
            print "Frequency: ", audio_info[0]
            print "Format: ", audio_info[1]
            print "Channels: ", audio_info[2]
            print "Number of mixer channels: ", pygame.mixer.get_num_channels()
        
    def run(self):
        fpsUpdateCounter = 0
        
        # game loop
        while 1:
            self.handlePyGameEvents()

            if self.sceneMgr.endGame:
                break
            self.sceneMgr.update()
            self.sceneMgr.draw()
            
            self.screenEffectsMgr.update()
            self.screenEffectsMgr.draw()
            
            if self.scaleFilter == SCALE_FILTER_SMOOTH:
                pygame.transform.smoothscale(self.screen, self.size, self.backbuffer)
            else:
                pygame.transform.scale(self.screen, self.size,self.backbuffer)
            
            pygame.display.flip()
            self.clock.tick(self.framerate)
            fpsUpdateCounter = fpsUpdateCounter + 1
            if fpsUpdateCounter > self.framerate:
                fpsUpdateCounter = 0
                pygame.display.set_caption('%s, FPS: %f' % (self.gameTitle, self.clock.get_fps()))
            if self.requestQuit == True:
                break
                    
        print "The Endo"
        
    def handlePyGameEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                #if event.key == pygame.K_ESCAPE:
                #    self.requestQuit = True
                #else:
                self.sceneMgr.key_down(event.key)
            elif event.type == pygame.KEYUP:
                self.sceneMgr.key_up(event.key)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.sceneMgr.mouse_key_down(event)
            elif event.type == pygame.MOUSEBUTTONUP:
                self.sceneMgr.mouse_key_up(event)
            elif event.type == pygame.MOUSEMOTION:
                self.sceneMgr.mouse_move(event)
                
##            
##    def getGameInfo(self):
##        return self.gameInfo
                    
                    
