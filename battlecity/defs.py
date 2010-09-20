## Project: BattleCity
## Module: Definitions
## Author: Salwan

import pygame

# game defs
GAME_LEVEL_COUNT = 50
TIME_STEP = 1.0 / 60.0
EAGLE_ADJ = [(5,11),(6,11),(7,11),(5,12),(7,12)]

# Tank direction
TANK_UP = 0
TANK_RIGHT = 2
TANK_DOWN = 4
TANK_LEFT = 6

# enum TileType
TILE_TYPE_NONE = 0
TILE_TYPE_BRICK = 1
TILE_TYPE_STONE = 2
TILE_TYPE_TREE = 3
TILE_TYPE_WATER = 4
TILE_TYPE_ICE = 5
TILE_TYPE_EAGLE = 6
TILE_TYPE_EAGLE_DESTROYED = 7
TILE_TYPE_STAR = 8
TILE_TYPE_BOMB = 9
TILE_TYPE_SHIELD = 10
TILE_TYPE_LIFE = 11
TILE_TYPE_RAFT = 12
TILE_TYPE_GUN = 13
TILE_TYPE_SHIELD_EAGLE = 14
TILE_TYPE_TIMER = 15
WINDOW_CONSTRUCT = 16
WINDOW_SAVE_LEVEL = 17
WINDOW_LOAD_LEVEL = 18
TEXT_LEVEL_NUMBER = 19
TEXT_LEVEL_NUMBER_LEFT = 20
TEXT_LEVEL_NUMBER_RIGHT = 21
BUTTON_YES = 22
BUTTON_NO = 23

INTERFACE_FLAG = 24
INTERFACE_ENEMY = 25
INTERFACE_PLAYER = 26

CURSOR_TANK_1 = 27
CURSOR_TANK_2 = 28

GAME_PLACEHOLDER_8 = 29
GAME_PLACEHOLDER_16 = 30
GAME_PLAYER_TANK_1 = 31
GAME_PLAYER_TANK_2 = 32
GAME_PLAYER_TANK_3 = 33
GAME_PLAYER_TANK_4 = 34
GAME_ENEMY_1_TANK = 35
GAME_ENEMY_2_TANK = 36
GAME_ENEMY_3_TANK = 37
GAME_ENEMY_4_TANK = 38

TANK_PAL_NONE = 100
TANK_PAL_METAL = 101
TANK_PAL_ORANGE = 102
TANK_PAL_GREEN = 103
TANK_PAL_RED = 104
TANK_SPAWN_EFFECT = 105
TANK_SHIELD_EFFECT = 106

TANK_CANNON_SHELL_UP = 107
TANK_CANNON_SHELL_DOWN = 108
TANK_CANNON_SHELL_LEFT = 109
TANK_CANNON_SHELL_RIGHT = 110

ENEMY_SHIELD_NONE = 111
ENEMY_SHIELD_ITEM = 112
ENEMY_SHIELD_FULL = 113
ENEMY_SHIELD_FULL_ITEM = 114

IMPACT_EXPLOSION_1 = 130
IMPACT_EXPLOSION_2 = 131
IMPACT_EXPLOSION_3 = 132
IMPACT_EXPLOSION_4 = 133
IMPACT_EXPLOSION_5 = 134

# Types
ENTITY_TYPE_TANK = 150
ENTITY_TYPE_PLAYER_TANK = 151
ENTITY_TYPE_CANNON_SHELL = 152
ENTITY_TYPE_TRANSPARENT = 153
ENTITY_TYPE_ITEM_STOPWATCH = 154
ENTITY_TYPE_ITEM_STAR = 155
ENTITY_TYPE_ITEM_HELMET = 156
ENTITY_TYPE_ITEM_GRENADE = 157
ENTITY_TYPE_ITEM_SHOVEL = 158
ENTITY_TYPE_ITEM_TANK = 159

GAME_OVER_POPUP = 160
GAME_SCORE_100 = 161
GAME_SCORE_200 = 162
GAME_SCORE_300 = 163
GAME_SCORE_400 = 164
GAME_SCORE_500 = 165
GAME_OVER_BANNER = 166

TANK_TYPE_PLAYER1 = 170
TANK_TYPE_PLAYER2 = 171
TANK_TYPE_PLAYER3 = 172
TANK_TYPE_PLAYER4 = 173

WARNING_SIGN = 174


# Data dictionaries
GameData = {
                GAME_PLACEHOLDER_8:     pygame.Rect(16, 104, 8, 8),
                GAME_PLACEHOLDER_16:    pygame.Rect(0, 112, 16, 16),
                GAME_PLAYER_TANK_1:     pygame.Rect(0, 112, 16, 16),
                GAME_PLAYER_TANK_2:     pygame.Rect(0, 128, 16, 16),
                GAME_PLAYER_TANK_3:     pygame.Rect(0, 144, 16, 16),
                GAME_PLAYER_TANK_4:     pygame.Rect(0, 160, 16, 16),
                GAME_ENEMY_1_TANK:      pygame.Rect(0, 176, 16, 16),
                GAME_ENEMY_2_TANK:      pygame.Rect(0, 192, 16, 16),
                GAME_ENEMY_3_TANK:      pygame.Rect(0, 208, 16, 16),
                GAME_ENEMY_4_TANK:      pygame.Rect(0, 224, 16, 16),
                TANK_SPAWN_EFFECT:      pygame.Rect(128, 80, 16, 16),
                TANK_SHIELD_EFFECT:     pygame.Rect(192, 80, 16, 16),
                TANK_CANNON_SHELL_UP:   pygame.Rect(48, 96, 3, 4),
                TANK_CANNON_SHELL_DOWN: pygame.Rect(48, 104, 3, 4),
                TANK_CANNON_SHELL_LEFT: pygame.Rect(56, 96, 4, 3),
                TANK_CANNON_SHELL_RIGHT:   pygame.Rect(56, 104, 4, 3),
                IMPACT_EXPLOSION_1:     pygame.Rect(128, 96, 16, 16),
                IMPACT_EXPLOSION_2:     pygame.Rect(144, 96, 16, 16),
                IMPACT_EXPLOSION_3:     pygame.Rect(160, 96, 16, 16),
                IMPACT_EXPLOSION_4:     pygame.Rect(176, 96, 32, 32),
                IMPACT_EXPLOSION_5:     pygame.Rect(208, 96, 32, 32),
                GAME_OVER_POPUP:        pygame.Rect(224, 16, 32, 16),
                GAME_SCORE_100:         pygame.Rect(176, 224, 16, 16),
                GAME_SCORE_200:         pygame.Rect(192, 224, 16, 16),
                GAME_SCORE_300:         pygame.Rect(208, 224, 16, 16),
                GAME_SCORE_400:         pygame.Rect(224, 224, 16, 16),
                GAME_SCORE_500:         pygame.Rect(240, 224, 16, 16),
                ENTITY_TYPE_ITEM_STOPWATCH: pygame.Rect(160, 208, 16, 16),
                ENTITY_TYPE_ITEM_STAR:  pygame.Rect(176, 208, 16, 16),
                ENTITY_TYPE_ITEM_HELMET: pygame.Rect(192, 208, 16, 16),
                ENTITY_TYPE_ITEM_GRENADE: pygame.Rect(208, 208, 16, 16),
                ENTITY_TYPE_ITEM_SHOVEL: pygame.Rect(224, 208, 16, 16),
                ENTITY_TYPE_ITEM_TANK:  pygame.Rect(240, 208, 16, 16),
                GAME_OVER_BANNER:       pygame.Rect(128,128,128,80),
}
MenuData = {
                CURSOR_TANK_1:   pygame.Rect(0, 80, 16, 16),
                CURSOR_TANK_2:   pygame.Rect(16, 80, 16, 16)
}
StripData = {
                GAME_ENEMY_1_TANK:     pygame.Rect(0, 176, 128, 16),
                GAME_ENEMY_2_TANK:     pygame.Rect(0, 192, 128, 16),
                GAME_ENEMY_3_TANK:     pygame.Rect(0, 208, 128, 16),
                GAME_ENEMY_4_TANK:     pygame.Rect(0, 224, 128, 16),
                GAME_PLAYER_TANK_1:     pygame.Rect(0, 112, 128, 16),
                GAME_PLAYER_TANK_2:     pygame.Rect(0, 128, 128, 16),
                GAME_PLAYER_TANK_3:     pygame.Rect(0, 144, 128, 16),
                GAME_PLAYER_TANK_4:     pygame.Rect(0, 160, 128, 16),
}

# Format: (tile id, src rect)
TilesData = {
                TILE_TYPE_EAGLE:    pygame.Rect(32, 80, 16, 16),
                TILE_TYPE_EAGLE_DESTROYED: pygame.Rect(80, 80, 16, 16),
                TILE_TYPE_BRICK:    pygame.Rect(8, 96, 8, 8),
                TILE_TYPE_STONE:    pygame.Rect(16, 96, 8, 8),
                TILE_TYPE_TREE:     pygame.Rect(24, 96, 8, 8),
                TILE_TYPE_WATER:    pygame.Rect(0, 104, 16, 8),
                TILE_TYPE_ICE:      pygame.Rect(32, 96, 8, 8),
}
InterfaceData = {
                INTERFACE_FLAG:     pygame.Rect(48, 80, 16, 16),
                INTERFACE_ENEMY:    pygame.Rect(16, 104, 8, 8),
                INTERFACE_PLAYER:   pygame.Rect(24, 104, 8, 8),
                WARNING_SIGN:       pygame.Rect(112, 70, 132, 10),
}

# Tank color palettes
TankPalette = {
                TANK_PAL_NONE:      [],
                TANK_PAL_METAL:     [(0x000000, 0x305080), (0x808080, 0xBCBCBC)],
                TANK_PAL_ORANGE:    [(0x808080, 0xFFA000), (0xFFFFFF, 0xFFF090), (0x000000, 0x888800)],
                TANK_PAL_RED:       [(0x808080, 0xE05000), (0x000000, 0x982078)],
                TANK_PAL_GREEN:     [(0xFFFFFF, 0xA0FFC8), (0x808080, 0x48A068), (0x000000, 0x386C00)],
}

# Enemy scores
ScoreForEnemy = {
                GAME_ENEMY_1_TANK:100,
                GAME_ENEMY_2_TANK:200,
                GAME_ENEMY_3_TANK:300,
                GAME_ENEMY_4_TANK:400
}

# Player controls
CONTROL_LEFT = 200
CONTROL_RIGHT = 201
CONTROL_UP = 202
CONTROL_DOWN = 203
CONTROL_FIRE = 204

PlayerKeyboardControls = {
                1:      {
                            CONTROL_LEFT:   pygame.K_LEFT, 
                            CONTROL_RIGHT:  pygame.K_RIGHT,
                            CONTROL_UP:     pygame.K_UP,
                            CONTROL_DOWN:   pygame.K_DOWN,
                            CONTROL_FIRE:   [pygame.K_SPACE, pygame.K_RCTRL],
                        },
                2:      {
                            CONTROL_LEFT:   pygame.K_a,
                            CONTROL_RIGHT:  pygame.K_d,
                            CONTROL_UP:     pygame.K_w,
                            CONTROL_DOWN:   pygame.K_s,
                            CONTROL_FIRE:   [pygame.K_LCTRL],
                        }
}

def setTankPalette(tank_surface, palette_type):
    pixel_array = pygame.PixelArray(tank_surface)
    for i in TankPalette[palette_type]:
        pixel_array.replace(i[0], i[1])
    pixel_array = None