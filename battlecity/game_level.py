## Project: BattleCity
## Module: Game Level
## Author: Salwan

import battlecity.entities.cannon_shell
import random
import pygame, os
import battlecity.map
import battlecity.level
import battlecity.entities.tank_spawner
from battlecity.controllers.player_controller import *
from battlecity.controllers.enemy_controller import *
from battlecity.entities import *
from battlecity.defs import *
from battlecity.entities.image_entity import *
from pyenkido.math_utils import *

ENEMY_SPAWN_PERIOD = 60 * 2
PLAYER_SPAWN_PERIOD = 60

WARNING_PERIOD = 60 * 3
WARNING_BLINK_RATE = 30

class GameLevel(battlecity.level.Level):
    def __init__(self, scene, screen, bitmap, level):
        super(GameLevel, self).__init__(screen, bitmap, level)
        self.scene = scene
        self.createLevel()
        self.spawnSlot = 0
        self.spawnTicks = ENEMY_SPAWN_PERIOD - 30
        self.spawnedEnemies = []
        self.player1SpawnTicks = PLAYER_SPAWN_PERIOD     
        self.player2SpawnTicks = PLAYER_SPAWN_PERIOD
        self.isGameOver = False
        self.gameOverPopup = self.bitmap.subsurface(GameData[GAME_OVER_POPUP])
        self.gameOverPopupPos = ((screen.get_width() / 2) - (GameData[GAME_OVER_POPUP].width / 2), screen.get_height())
        self.gameOverPopupTargetY = (screen.get_height() / 2) - (GameData[GAME_OVER_POPUP].height / 2)
        self.gameOverWait = 100
        self.p1Lives = self.scene.sceneMgr.gamedb["Lives"][1]
        self.p2Lives = self.scene.sceneMgr.gamedb["Lives"][2]
        self.playerCount = self.scene.sceneMgr.gamedb["PlayerCount"]
        self.playersAlive = self.scene.sceneMgr.gamedb["PlayersAlive"]

        # 2-player mode specific gameover
        self.isPlayerGameOver = False
        self.playerGameOverPos = (0, 0)
        self.playerGameOverTargetX = 0
        self.playerGameOverWait = 100
        
        self.isLevelWon = False
        self.levelWonWait = 180        

        # Sounds
        self.itemAppearSound = pyenkido.sound.load_sound("res/sounds", "item_appear.ogg")
        self.itemTankSound = pyenkido.sound.load_sound("res/sounds", "bonus_life.ogg")
        self.itemNormalSound = pyenkido.sound.load_sound("res/sounds", "item_take.ogg")

        # Cheats (used for development purposes)
        self.godMode = False

        # Item
        self.item = None
        self.shovelItem = None

        # Distribution of enemy tank types over levels to create a difficulty curve
        self.enemyPercent = {}
        final = self.scene.sceneMgr.gamedb["LevelCount"]
        third1 = final * 0.33
        third2 = final * 0.66
        # -- Type 1
        le = LinearEquation()
        le.addLine((1, 90), (final, 10))
        self.enemyPercent[0] = le.getY(self.scene.sceneMgr.gamedb["Level"])
        # -- Type 2
        le = LinearEquation()
        le.addLine((1, 10), (third1, 90))
        le.addLine((third1, 90), (final, 25))
        self.enemyPercent[1] = le.getY(self.scene.sceneMgr.gamedb["Level"])
        # -- Type 3
        le = LinearEquation()
        le.addLine((1, 10), (third2, 90))
        le.addLine((third2, 90),(final, 35))
        self.enemyPercent[2] = le.getY(self.scene.sceneMgr.gamedb["Level"])
        # -- Type 4
        le = LinearEquation()
        le.addLine((1, 10),(final, 90))
        self.enemyPercent[3] = le.getY(self.scene.sceneMgr.gamedb["Level"])
        # Randomization list
        self.randomEnemyPercent = [
                (0, int(self.enemyPercent[0])),
                (1, int(self.enemyPercent[1])),
                (2, int(self.enemyPercent[2])),
                (3, int(self.enemyPercent[3]))]
        print "Level:", self.scene.sceneMgr.gamedb["Level"]
        print ">> Enemy 1 percent:", self.enemyPercent[0]
        print ">> Enemy 2 percent:", self.enemyPercent[1]
        print ">> Enemy 3 percent:", self.enemyPercent[2]
        print ">> Enemy 4 percent:", self.enemyPercent[3]

        # Spawn players
        self.spawnNewPlayers()

        # Warning
        self.warningPeriod = WARNING_PERIOD
        self.warningBlinkRate = WARNING_BLINK_RATE
        self.isWarning = False
        self.warningBlink = 1
        self.warningText = self.bitmap.subsurface(InterfaceData[WARNING_SIGN])
        self.warningSound = pyenkido.sound.load_sound("res/sounds", "warning.ogg")

    def update(self):
        super(GameLevel, self).update()
        if not self.isGameOver:
            if not self.isLevelWon:
                self.spawnTicks += 1
                if self.spawnTicks >= ENEMY_SPAWN_PERIOD:
                    self.spawnTicks = 0
                    self.spawnNewEnemy()
                if 1 in self.playersAlive and not self.player_1.isAlive():
                    self.player1SpawnTicks -= 1
                    if self.player1SpawnTicks <= 0:
                        self.player1SpawnTicks = PLAYER_SPAWN_PERIOD
                        self.lostLife(self.player_1)
                        if self.p1Lives > 0:
                            self.spawnNewPlayer1()
                        else:
                            # Player 1 is no longer alive
                            self.endPlayer1()
                if 2 in self.playersAlive and not self.player_2.isAlive():
                    self.player2SpawnTicks -= 1
                    if self.player2SpawnTicks <= 0:
                        self.player2SpawnTicks = PLAYER_SPAWN_PERIOD
                        self.lostLife(self.player_2)
                        if self.p2Lives > 0:
                            self.spawnNewPlayer2()
                        else:
                            # Player 2 is no longer alive
                            self.endPlayer2()

                # Player game over
                if self.isPlayerGameOver:
                    if self.playerGameOverPos[0] != self.playerGameOverTargetX:
                        if self.playerGameOverPos[0] < self.playerGameOverTargetX:
                            self.playerGameOverPos = (self.playerGameOverPos[0] + 1, self.playerGameOverPos[1])
                        else:
                            self.playerGameOverPos = (self.playerGameOverPos[0] - 1, self.playerGameOverPos[1])
                    elif self.playerGameOverWait > 0:
                        self.playerGameOverWait -= 1
                    else:
                        self.isPlayerGameOver = False

                # Game Over
                if len(self.playersAlive) <= 0:
                    self.setGameOver()
            else:
                self.levelWonWait -= 1
                if self.levelWonWait <= 0:
                    # upgrade tanks level
                    if 1 in self.playersAlive and self.player_1:
                        self.scene.sceneMgr.gamedb["TankLevel"][1] = self.player_1.getTankLevel()
                    if 2 in self.playersAlive and self.player_2:
                        self.scene.sceneMgr.gamedb["TankLevel"][2] = self.player_2.getTankLevel()
                    self.scene.end()

            # Clear dead enemies
            if len(self.spawnedEnemies) > 0:
                to_remove = []
                for e in self.spawnedEnemies:
                    if not e.isAlive():
                        to_remove.append(e)
                for t in to_remove:
                    self.spawnedEnemies.remove(t)
                
        else:
            if self.gameOverPopupPos[1] > self.gameOverPopupTargetY:
                self.gameOverPopupPos = (self.gameOverPopupPos[0], self.gameOverPopupPos[1] - 1)
            elif self.gameOverWait > 0:
                self.gameOverWait -= 1
            else:
                self.gameOver()

        # Check item
        if self.item != None:
            if not self.item.isAlive():
                self.item = None
            else:
                coll_list = self.collideEntities(self.item.rect)
                if len(coll_list) > 0:
                    for e in coll_list:
                        if e.type == ENTITY_TYPE_PLAYER_TANK:
                            if self.item.type == ENTITY_TYPE_ITEM_TANK:
                                self.takeTankItem(e, self.item.rect)
                            elif self.item.type == ENTITY_TYPE_ITEM_SHOVEL:
                                self.takeShovelItem(e, self.item.rect)
                            elif self.item.type == ENTITY_TYPE_ITEM_GRENADE:
                                self.takeGrenadeItem(e, self.item.rect)
                            elif self.item.type == ENTITY_TYPE_ITEM_HELMET:
                                self.takeHelmetItem(e, self.item.rect)
                            elif self.item.type == ENTITY_TYPE_ITEM_STAR:
                                self.takeStarItem(e, self.item.rect)
                            elif self.item.type == ENTITY_TYPE_ITEM_STOPWATCH:
                                self.takeStopWatchItem(e, self.item.rect)
                            self.item.kill()
                            self.item = None

        # Handle warning
        if self.isWarning and not self.isGameOver:
            self.warningPeriod -= 1
            self.warningBlinkRate -= 1
            if self.warningPeriod <= 0:
                self.isWarning = False
                self.warningPeriod = WARNING_PERIOD
            if self.warningBlinkRate <= 0:
                self.warningBlinkRate = WARNING_BLINK_RATE
                self.warningBlink = 1 - self.warningBlink

    def draw(self):
        super(GameLevel, self).draw()
        if self.isGameOver:
            self.screen.blit(self.gameOverPopup, self.gameOverPopupPos)

        if self.isPlayerGameOver:
            self.screen.blit(self.gameOverPopup, self.playerGameOverPos)

        # Draw warning
        if self.isWarning and not self.isGameOver and self.warningBlink == 1:
            self.screen.blit(self.warningText, (54, 226))
            
    def endPlayer1(self):
        self.playersAlive.remove(1)
        self.scene.sceneMgr.gamedb["PlayersAlive"] = self.playersAlive

        if len(self.playersAlive) > 0:
            # player 1 specific game over
            self.isPlayerGameOver = True
            self.playerGameOverPos = (-32, 208)
            self.playerGameOverTargetX = 72
            self.playerGameOverWait = 100

    def endPlayer2(self):
        self.playersAlive.remove(2)
        self.scene.sceneMgr.gamedb["PlayersAlive"] = self.playersAlive

        if len(self.playersAlive) > 0:
            # player 2 specific game over
            self.isPlayerGameOver = True
            self.playerGameOverPos = (256 + 32, 208)
            self.playerGameOverTargetX = 137
            self.playerGameOverWait = 100

    def collideEntities(self, rect):
        dummy_sprite = pygame.sprite.Sprite()
        dummy_sprite.rect = rect
        return pygame.sprite.spritecollide(dummy_sprite, self.entities, False)

    def collideEntitiesSpawn(self, rect):
        sprites = self.collideEntities(rect)
        for s in sprites:
            if s.type == ENTITY_TYPE_TANK or s.type == ENTITY_TYPE_PLAYER_TANK:
                return True
        return False

    def collideCannonShellMap(self, rect):
        dummy_sprite = pygame.sprite.Sprite()
        dummy_sprite.rect = rect
        return pygame.sprite.spritecollide(dummy_sprite, self.map.tilesGroup, False, self.cannonShellMapCollider)


    def cannonShellMapCollider(self, sprite1, sprite2):
        if type(sprite2) is battlecity.entities.brick.Brick:
            return sprite2.collideRect(sprite1.rect)
        else:
            return sprite1.rect.colliderect(sprite2.rect)

    def collideIce(self, rect):
        dummy_sprite = pygame.sprite.Sprite()
        dummy_sprite.rect = rect
        return pygame.sprite.spritecollide(dummy_sprite, self.map.tilesGroup, False, self.iceMapCollider)

    def iceMapCollider(self, sprite1, sprite2):
        if type(sprite1) is battlecity.entities.ice.Ice or type(sprite2) is battlecity.entities.ice.Ice:
            return sprite1.rect.colliderect(sprite2.rect)
        else:
            return False
        
    def spawnNewPlayers(self):
        if 1 in self.playersAlive:
            self.spawnNewPlayer1()
        if 2 in self.playersAlive:
            self.spawnNewPlayer2()

    def spawnNewPlayer1(self):
        self.player_1 = player_tank.PlayerTank(self.bitmap, self, self.scene.sceneMgr.gamedb["TankLevel"][1], 1, self.scene.playerTextures)
        self.player_1.setPosition((80, 208))
        p1Controller = PlayerController()
        self.scene.attachControllerToEntity(p1Controller, self.player_1)
        spawner = battlecity.entities.tank_spawner.TankSpawner(self.bitmap, self.player_1, self.entities, (80, 208))
        self.entities.add(spawner)

    def spawnNewPlayer2(self):
        self.player_2 = player_tank.PlayerTank(self.bitmap, self, self.scene.sceneMgr.gamedb["TankLevel"][2], 2, self.scene.playerTextures)
        self.player_2.setPosition((144, 208))
        p2Controller = PlayerController()
        self.scene.attachControllerToEntity(p2Controller, self.player_2)
        spawner = battlecity.entities.tank_spawner.TankSpawner(self.bitmap, self.player_2, self.entities, (144, 208))
        self.entities.add(spawner)

    def spawnNewEnemy(self):
        # 4 tanks in single player mode
        enemyCount = 4
        # 6 tanks in 2 player mode
        if self.playerCount == 2:
            enemyCount = 6

        if self.enemyCount <= 0:
            if len(self.spawnedEnemies) <= 0:
                self.isLevelWon = True
            return

        if len(self.spawnedEnemies) >= enemyCount:
            return

        rc = None
        if self.spawnSlot == 0:
            rc = pygame.rect.Rect(16, 16, 16, 16)
        elif self.spawnSlot == 1:
            rc = pygame.rect.Rect(112, 16, 16, 16)
        elif self.spawnSlot == 2:
            rc = pygame.rect.Rect(208, 16, 16, 16)
        else:
            self.spawnSlot = 0
            return
        self.spawnSlot += 1
        if  self.collideEntitiesSpawn(rc):
            self.spawnTicks = ENEMY_SPAWN_PERIOD
            return
        else:
            r_type = get_random_percent(self.randomEnemyPercent)
            r_item = get_random_percent([(0, 80), (1,20)])
            r_shield = ENEMY_SHIELD_NONE
            if r_type == 3: # last tank type is always full shielded
                if r_item:
                    r_shield = ENEMY_SHIELD_FULL_ITEM
                else:
                    r_shield = ENEMY_SHIELD_FULL
            else: # other tank types don't have a shield
                if r_item:
                    r_shield = ENEMY_SHIELD_ITEM
                else:
                    r_shield = ENEMY_SHIELD_NONE

            enemy =  enemy_tank.EnemyTank(self.bitmap, self, GAME_ENEMY_1_TANK + r_type, r_shield, self.scene.enemyTextures)
            enemy.setPosition(rc.topleft)
            enemyController = EnemyController()
            self.scene.attachControllerToEntity(enemyController, enemy)
            self.spawnedEnemies.append(enemy)
            spawner = battlecity.entities.tank_spawner.TankSpawner(self.bitmap, enemy, self.entities, rc.topleft)
            self.entities.add(spawner)
            self.enemyCount -= 1

    def setGameOver(self):
        self.isGameOver = True
        if 1 in self.playersAlive:
            if self.player_1 and self.player_1.controller:
                self.scene.removeController(self.player_1.controller)
        if 2 in self.playersAlive:
            if self.player_2 and self.player_2.controller:
                self.scene.removeController(self.player_2.controller)

    def gameOver(self):
        self.scene.gameOver()
        self.scene.end()

    def pauseGame(self):
        if self.isLevelWon or self.isGameOver:
            return
        self.scene.pauseGame()

    def resumeGame(self):
        if self.isLevelWon or self.isGameOver:
            return
        self.scene.resumeGame()

    def lostLife(self, player):
        pl = "Player" + str(player.playerNum) + "Level"
        self.scene.sceneMgr.gamedb[pl] = GAME_PLAYER_TANK_1
        if player.playerNum == 1:
            self.p1Lives -= 1
        elif player.playerNum == 2:
            self.p2Lives -= 1

    def checkWarning(self, tile):
        if tile.isEagleWall() and not self.isWarning:
            self.isWarning = True
            self.warningPeriod = WARNING_PERIOD
            self.warningBlinkRate = WARNING_BLINK_RATE
            self.warningSound.play()

    def spawnItem(self):
        self.itemAppearSound.play()
        x = random.randint(0, 159) + 32
        y = random.randint(0, 159) + 32
        t = random.randint(0, 5)
        it = battlecity.entities.item_entity.ItemEntity(self.bitmap, (x, y), ENTITY_TYPE_ITEM_STOPWATCH + t)
        if self.item != None and self.item.isAlive():
            if self.item.isAlive() and self.item:
                self.item.kill()
            self.item = None
        self.item = it
        self.entities.add(it)

    def addFragScore(self, who, victim_tank_type, rect):
        if victim_tank_type not in self.scene.sceneMgr.gamedb["FragList"][who.playerNum]:
            self.scene.sceneMgr.gamedb["FragList"][who.playerNum][victim_tank_type] = 1
        else:
            self.scene.sceneMgr.gamedb["FragList"][who.playerNum][victim_tank_type] += 1
        score_image = None
        if victim_tank_type == GAME_ENEMY_1_TANK:
            score_image = self.bitmap.subsurface(GameData[GAME_SCORE_100])
        elif victim_tank_type == GAME_ENEMY_2_TANK:
            score_image = self.bitmap.subsurface(GameData[GAME_SCORE_200])
        elif victim_tank_type == GAME_ENEMY_3_TANK:
            score_image = self.bitmap.subsurface(GameData[GAME_SCORE_300])
        elif victim_tank_type == GAME_ENEMY_4_TANK:
            score_image = self.bitmap.subsurface(GameData[GAME_SCORE_400])

        self.scene.sceneMgr.gamedb["Score"][who.playerNum] += ScoreForEnemy[victim_tank_type]
        score_image_ent = ImageEntityTimeKill(score_image, rect.topleft, ENTITY_TYPE_TRANSPARENT, 60)
        self.entities.add(score_image_ent)

    def addItemScore(self, who, rect):
        self.scene.sceneMgr.gamedb["Score"][who.playerNum] += 500
        if rect != None:
            score_image_ent = ImageEntityTimeKill(self.bitmap.subsurface(GameData[GAME_SCORE_500]), rect.topleft, ENTITY_TYPE_TRANSPARENT, 60, 10)
            self.entities.add(score_image_ent)

    def takeTankItem(self, who, rect):
        self.itemTankSound.play()
        self.addItemScore(who, rect)
        if who.playerNum == 1:
            self.p1Lives += 1
        elif who.playerNum == 2:
            self.p2Lives += 1

    def takeShovelItem(self, who, rect):
        if self.shovelItem:
            self.shovelItem.kill()
            self.shovelItem = None
        self.itemNormalSound.play()
        self.addItemScore(who, rect)
        shovel_ent = battlecity.entities.shovel_action.ShovelAction(self, self.map)
        self.entities.add(shovel_ent)
        self.shovelItem = shovel_ent

    def takeGrenadeItem(self, who, rect):
        if who.type == ENTITY_TYPE_PLAYER_TANK:
            self.itemNormalSound.play()
            self.addItemScore(who, rect)
            for t in self.spawnedEnemies:
                if t.isSpawned:
                    t.takeDamage(None, 5)
                #if not t.isAlive():
                #    self.addFragScore(t.tankType, t.rect)

    def takeHelmetItem(self, who, rect):
        if who.type == ENTITY_TYPE_PLAYER_TANK:
            who.giveShield(60 * 8)
            self.itemNormalSound.play()
            self.addItemScore(who, rect)

    def takeStarItem(self, who, rect):
        if who.type == ENTITY_TYPE_PLAYER_TANK:
            who.upgradeTank()
            self.itemNormalSound.play()
            self.addItemScore(who, rect)
            pl = "Player" + str(who.playerNum) + "Level"
            self.scene.sceneMgr.gamedb[pl] = who.tankLevel

    def takeStopWatchItem(self, who, rect):
        if who.type == ENTITY_TYPE_PLAYER_TANK:
            self.itemNormalSound.play()
            self.addItemScore(who, rect)
            for t in self.spawnedEnemies:
                t.setStopWatch(60 * 9)
            

