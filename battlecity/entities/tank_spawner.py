## Project: battlecity
## Module: Tank entity Spawner
## Author: Salwan

import pygame
from battlecity.defs import *
from pyenkido.entity_spawner import *

# settings
SPAWN_FRAME_DELAY = 3

# Spawn sequence
SpawnSequence = [0, 1, 2, 3, 2, 1, 0, 1, 2, 3, 2, 1, 0]

class TankSpawner(EntitySpawner):
    def __init__(self, bitmap, entity_to_spawn, group, pos):
        super(TankSpawner, self).__init__(entity_to_spawn, group)
        if entity_to_spawn.controller:
            entity_to_spawn.controller.deactivate()
        self.bitmap = bitmap
        self.hasSpawned = False
        self.spawnImages = []
        rc = GameData[TANK_SPAWN_EFFECT].copy()
        for i in range(0, 4):
            self.spawnImages.append(self.bitmap.subsurface(rc))
            rc.left += 16
        self.currentSpawnFrame = 0
        self.spawnTicks = 0
        self.image = self.spawnImages[0]
        self.rect = (pos[0], pos[1], 16, 16)

    def update(self):
        if self.currentSpawnFrame < len(SpawnSequence):
            self.image = self.spawnImages[SpawnSequence[self.currentSpawnFrame]]
            self.spawnTicks += 1
            if self.spawnTicks > SPAWN_FRAME_DELAY:
                self.currentSpawnFrame += 1
                self.spawnTicks = 0
        else:
            self.spawnEntity()
