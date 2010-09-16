## Project: BattleCity
## Module: Map
## Author: Salwan

import pygame, math, pickle
from battlecity.defs import *
from battlecity.entities import *

# Dealing with py2exe bug
import battlecity.entities.tank
import battlecity.entities.player_tank
import battlecity.entities.enemy_tank
import battlecity.entities.eagle
import battlecity.entities.brick
import battlecity.entities.cannon_shell
import battlecity.entities.explosion
import battlecity.entities.ice
import battlecity.entities.image_entity
import battlecity.entities.item_entity
import battlecity.entities.shovel_action
import battlecity.entities.stone
import battlecity.entities.tank_spawner
import battlecity.entities.tile
import battlecity.entities.tree
import battlecity.entities.water

class Map:
    def __init__(self, bitmap):
        self.bitmap = bitmap
        self.clearMap()

    def save(self, file):
        #pickle.dump(self.tiles, file, pickle.HIGHEST_PROTOCOL)
        #pickle.dump(self.objects, file, pickle.HIGHEST_PROTOCOL)
        tileData = []
        for y in range(0, 26):
            for x in range(0, 26):
                tile = self.getTile((x, y))
                if tile is None:
                    tileData.append(TILE_TYPE_NONE)
                else:
                    tileData.append(tile.type)
        pickle.dump(tileData, file, pickle.HIGHEST_PROTOCOL)

    def load(self, file):
        self.clearMap()
        tileData = pickle.load(file)
        for y in range(0, 26):
            for x in range(0, 26):
                self.createTile((x, y), tileData[x + (y * 26)])
        
    def update(self):
        sprites = self.tilesGroup.sprites()
        for s in sprites:
            s.update()

    def preDraw(self, screen):
        for t in self.tilesGroup:
            t.preDraw(screen)
        
    def draw(self, screen):        
        self.tilesGroup.draw(screen)

    def postDraw(self, screen):
        for t in self.tilesGroup:
            t.postDraw(screen)

    def createTile(self, at, type):
        tile = None
        if type == TILE_TYPE_NONE:
            return
        elif type == TILE_TYPE_BRICK:
            tile = brick.Brick(self.tilesGroup, self.bitmap, (0, 0))
        elif type == TILE_TYPE_WATER:
            tile = water.Water(self.tilesGroup, self.bitmap, (0, 0))
        elif type == TILE_TYPE_STONE:
            tile = stone.Stone(self.tilesGroup, self.bitmap, (0, 0))
        elif type == TILE_TYPE_ICE:
            tile = ice.Ice(self.tilesGroup, self.bitmap, (0, 0))
        elif type == TILE_TYPE_TREE:
            tile = tree.Tree(self.tilesGroup, self.bitmap, (0, 0))
        self.setTile(at, tile)

    def clearMap(self):
        self.tiles = []
        for i in range(0, 26 * 26):
            self.tiles.append(None)
        self.objects = []
        for i in range(0, 13 * 13):
            self.objects.append(None)
        self.tilesGroup = pygame.sprite.LayeredUpdates()
        # Eagle must exist always
        base = eagle.Eagle(self.tilesGroup, self.bitmap, pygame.Rect(0, 0, 16, 16), TILE_TYPE_EAGLE, 0)
        self.setObject((6, 12), base)
        
    def setObject(self, at, tile):
        self.objects[at[0] + (at[1] * 13)] = tile
        tile.setPosition(( 16 + (at[0] * 16), 16 + (at[1] * 16) ))

    def clearObject(self, at):
        if self.objects[at[0] + (at[1] * 13)] != None:
            self.tilesGroup.remove(self.objects[at[0] + (at[1] * 13)])
        self.objects[at[0] + (at[1] * 13)] = None
        
    def getObject(self, at):
        return self.objects[at[0] + (at[1] * 13)]
    
    def setTile(self, at, tile):
        self.tiles[at[0] + (at[1] * 26)] = tile
        tile.setPosition(( 16 + (at[0] * 8), 16 + (at[1] * 8) ))

    def clearTile(self, at):
        if self.tiles[at[0] + (at[1] * 26)] != None:
            self.tilesGroup.remove(self.tiles[at[0] + (at[1] * 26)])
        self.tiles[at[0] + (at[1] * 26)] = None

    def clear4Tiles(self, at):
        att = [(at[0] * 2, at[1] * 2),
            (1 + at[0] * 2, at[1] * 2),
            (at[0] * 2, 1 + at[1] * 2),
            (1 + at[0] * 2, 1 + at[1] * 2)]
        for a in att:
            self.clearTile(a)
    
    def getTile(self, at):
        return self.tiles[at[0] + (at[1] * 26)]

    def getTileCoords(self, pos):
        return ((pos[0] - 16) / 8, (pos[1] - 16) / 8)

    def getObjectCoords(self, pos):
        return ((pos[0] - 16) / 16, (pos[1] - 16) / 16)

    def getTileType(self, at):
        return self.getTile(at).type

    def getObjectType(self, at):
        obj = self.getObject(at)
        if obj != None:
            return obj.type
        else:
            return TILE_TYPE_NONE

        
        
        
