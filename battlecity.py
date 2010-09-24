## Project: Battle City Remake
## Author: Salwan Asaad
## Main

# Use psyco JIT compiler
import psyco
psyco.full()


import pyenkido.startup
import pyenkido.game
from pyenkido.preferences import *
import battlecity.scenes.introduction
import battlecity.scenes.black_transition
import battlecity.scenes.mainmenu
import battlecity.scenes.level_display
import battlecity.scenes.level_scene
import battlecity.scenes.construct_level
import battlecity.scenes.level_score
import battlecity.scenes.game_over
import battlecity.scenes.new_hiscore

class BattleCityStartup(pyenkido.startup.Startup):
    def prepareScenes(self):
        self.sceneMgr.add_scene("Intro", battlecity.scenes.introduction.IntroScene(self.sceneMgr, self.screen))
        self.sceneMgr.add_scene("IntroBlackTransition", battlecity.scenes.black_transition.IntroBlackTransitionScene(self.sceneMgr, self.screen))
        self.sceneMgr.add_scene("GameMainMenu", battlecity.scenes.mainmenu.MainMenuScene(self.sceneMgr, self.screen))
        self.sceneMgr.add_scene("LevelDisplay", battlecity.scenes.level_display.LevelDisplay(self.sceneMgr, self.screen))
        self.sceneMgr.add_scene("LevelScene", battlecity.scenes.level_scene.LevelScene(self.sceneMgr, self.screen))
        self.sceneMgr.add_scene("LevelEditor", battlecity.scenes.construct_level.ConstructLevel(self.sceneMgr, self.screen))
        self.sceneMgr.add_scene("LevelScore", battlecity.scenes.level_score.LevelScoreScene(self.sceneMgr, self.screen))
        self.sceneMgr.add_scene("GameOver", battlecity.scenes.game_over.GameOverScene(self.sceneMgr, self.screen))
        self.sceneMgr.add_scene("NewHiScore", battlecity.scenes.new_hiscore.NewHiScoreScene(self.sceneMgr, self.screen))
        self.sceneMgr.change_scene("Intro")

Preferences = pyenkido.game.GamePreferences()
Preferences.load("game.cfg")
Preferences.mouseVisible = False
Preferences.iconFile = "res/window_icon.png"
Game = pyenkido.game.Game(Preferences)
BattleCity = BattleCityStartup(Game)
Game.run()

