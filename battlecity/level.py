## Project: BattleCity
## Module: Level
## Author: Salwan

import pygame, os
import battlecity.map

class Level(object):
    def __init__(self, screen, bitmap, level = 1):
        self.screen = screen
        self.bitmap = bitmap
        self.map = battlecity.map.Map(bitmap)
        self.entities = pygame.sprite.LayeredUpdates()
        self.level = level
        self.enemyCount = 20

    def createLevel(self):
        path = "res/maps"
        filename = "%s.map" % (str(self.level))
        self.load(path, filename)
        
    def update(self):
        self.map.update()
        sprites = self.entities.sprites()
        for s in sprites:
            s.update()
        
    def draw(self):
        pygame.draw.rect(self.screen, (0, 0, 0), pygame.Rect(16, 16, 208, 208))
        sprites = self.entities.sprites()
        # Pre-Draw
        self.map.preDraw(self.screen)
        for s in sprites:
            s.preDraw(self.screen)

        # Drawing level
        self.entities.draw(self.screen)
        self.map.draw(self.screen)

        # Post-Draw
        self.map.postDraw(self.screen)
        for s in sprites:
            s.postDraw(self.screen)


    def gameOver(self):
        pass

    def game_paused(self):
        for e in self.entities:
            e.game_paused()

    def game_resumed(self):
        for e in self.entities:
            e.game_resumed()

    def spawnEntity(self, entity):
        self.entities.add(entity)
        entity.spawned()

    def collideMap(self, rect):
        dummy_sprite = pygame.sprite.Sprite()
        dummy_sprite.rect = rect
        return pygame.sprite.spritecollide(dummy_sprite, self.map.tilesGroup, False)

    def explosionDamage(self, rect):
        # Map collision
        coll_list = collideMap(rect)

    def save(self, path, filename):
        file = open(os.path.join(path, filename), "w")
        self.map.save(file)
        file.close()

    def load(self, path, filename):
        try:
            file = open(os.path.join(path, filename), "rb")
            self.map.load(file)
            file.close()
        except IOError:
            # could not open file, may be it doesn't exist or the format is wrong
            # create a new file and save it
            self.map = battlecity.map.Map(self.bitmap)
            self.save(path, filename)

        # Clear spawn points
        self.map.clear4Tiles((0, 0))
        self.map.clear4Tiles((6, 0))
        self.map.clear4Tiles((12, 0))
        self.map.clear4Tiles((4, 0))
        self.map.clear4Tiles((8, 0))
        
