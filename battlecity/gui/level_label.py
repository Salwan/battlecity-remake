## Project: BattleCity
## Module: GUI Control: Level Label
## Author: Salwan A. AlHelaly

import pyenkido.gui.label
from battlecity.defs import *

class LevelLabel(pyenkido.gui.label.Label):
    def __init__(self, at, start_level, color_mask = (1, 1, 1)):
        super(LevelLabel, self).__init__(at, str(start_level), color_mask, True)
        self.level = start_level
        if self.level < 1:
            self.level = 1
        if self.level > GAME_LEVEL_COUNT:
            self.level = GAME_LEVEL_COUNT

    def key_down(self, key):
        if key == pygame.K_UP or key == pygame.K_RIGHT:
            self.level += 1
            if self.level > GAME_LEVEL_COUNT:
                self.level = GAME_LEVEL_COUNT
            self.text = str(self.level)
        elif key == pygame.K_DOWN or key == pygame.K_LEFT:
            self.level -= 1
            if self.level < 1:
                self.level = 1
            self.text = str(self.level)

    def key_up(self, key):
        pass


