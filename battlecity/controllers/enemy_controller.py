## Project: BattleCity
## Module: enemy controller
## Author: Salwan

import pygame
import pyenkido.entity
import pyenkido.controller
import random
from pyenkido.math_utils import *

# constants
RandomMovementPercent = [(1,15),(2,20),(3,20),(4,45)]
RandomFirePercent = [(False,80),(True,5),(False,15)]

class EnemyController(pyenkido.controller.Controller):
    def __init__(self):
        super(EnemyController, self).__init__()
        self.ticks = 0
        self.changeDirectionPeriod = random.randint(10, 60)
        self.stopWatch = 0

    def update(self):
        if not self.entity or not self.active:
            return
        if self.stopWatch > 0:
            self.stopWatch -= 1
            return
        self.entity.move()

        # Changing Direction
        self.ticks += 1
        if self.ticks >= self.changeDirectionPeriod:
            self.ticks = 0
            self.changeDirectionPeriod = random.randint(10, 60)
            new_dir = get_random_percent(RandomMovementPercent)
            if new_dir == 1:
                self.entity.setUp()
            elif new_dir == 2:
                self.entity.setLeft()
            elif new_dir == 3:
                self.entity.setRight()
            else:
                self.entity.setDown()

        # Firing cannon
        should_fire = get_random_percent(RandomFirePercent)
        if should_fire:
            self.entity.fire()

    def setStopWatch(self, ticks):
        self.stopWatch = ticks
