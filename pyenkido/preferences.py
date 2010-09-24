## Project: pyEnkido
## Module: preferences
## Author: Salwan

import os, pickle

# enum SCALE_FILTER_TYPE
SCALE_FILTER_NONE = 0
SCALE_FILTER_SMOOTH = 1

class GamePreferences:
    fullscreen = False
    renderingResolution = (256, 240)
    displayResolution = (800, 600)
    mouseVisible = True
    scaleFilter = SCALE_FILTER_NONE
    framerate = 60
    alpha = False
    gameTitle = "PyEnkido Game Engine"
    iconFile = ""

    def save(self, filename):
        file = open(filename, "w")
        pickle.dump(self, file, pickle.HIGHEST_PROTOCOL)
        file.close()

    def load(self, filename):
        gamePrefs = GamePreferences()
        try:
            file = open(filename, "r")
            gamePrefs = pickle.load(file)
            file.close()
        except IOError, EOFError:
            gamePrefs.save(filename)

        self.fullscreen = gamePrefs.fullscreen
        self.renderingResolution = gamePrefs.renderingResolution
        self.displayResolution = gamePrefs.displayResolution
        self.moueVisible = gamePrefs.mouseVisible
        self.scaleFilter = gamePrefs.scaleFilter
        self.framerate = gamePrefs.framerate
        self.alpha = gamePrefs.alpha
        self.gameTitle = gamePrefs.gameTitle
        self.iconFile = gamePrefs.iconFile


