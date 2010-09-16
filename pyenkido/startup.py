## Project: pyEnkido
## Module: startup
## Author: Salwan

import pyenkido.game

class Startup:
    def __init__(self, game):
        self.game = game
        self.sceneMgr = game.sceneMgr
        self.screen = game.screen
        self.prepareScenes()
        
    def prepareScenes(self):
        pass
        
    