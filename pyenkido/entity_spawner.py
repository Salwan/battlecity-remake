## Project: pyEnkido
## Module: Entity Spawner
## Author: Salwan
"""
Spawns an entity when it's finished after a defined period of time.
Override update to define your own rules.
Spawning is done by adding the entity you gave to a group you supplied.
Kills itself after spawning the entity.
"""
import pygame
from pyenkido.entity import *

class EntitySpawner(Entity):
    def __init__(self, entity_to_spawn, group, period = 0):
        super(EntitySpawner, self).__init__()
        self.entity_to_spawn = entity_to_spawn
        self.group_to_use = group
        self.period = period

    def update(self):
        self.period -= 1
        if self.period <= 0:
            spawnEntity()

    def spawnEntity(self):
        self.group_to_use.add(self.entity_to_spawn)
        self.entity_to_spawn.spawned()
        self.kill()

