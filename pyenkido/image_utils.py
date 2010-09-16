# Project: BattleCity
# Module: None (image utilities)
# Author: Salwan A. AlHelaly

import os, sys, pygame, math

def sprite_split_bitmap(surface, sprite_width, sprite_height, sprites_per_row, sprite_count, first_sprite_y = 0):
    r = pygame.Rect(0,0,0,0)
    sprites = []
    for c in range(0, sprite_count):
        r = pygame.Rect( (c % sprites_per_row) * sprite_width, (math.floor(c / sprites_per_row) * sprite_height) + first_sprite_y, sprite_width, sprite_height)
        sprites.append(surface.subsurface(r))
    return sprites

def sprite_split_bitmap_mirror(surface, sprite_width, sprite_height, sprites_per_row, sprite_count, first_sprite_y = 0):
    r = pygame.Rect(0,0,0,0)
    w = surface.get_width() - sprite_width
    sprites = []
    for c in range(0, sprite_count):
        r = pygame.Rect( w - (c % sprites_per_row) * sprite_width, (math.floor(c / sprites_per_row) * sprite_height) + first_sprite_y, sprite_width, sprite_height)
        sprites.append(surface.subsurface(r))
    return sprites

def load_image(path, filename):
    return pygame.image.load(os.path.join(path,filename)).convert()

def load_image_alpha(path, filename):
    return pygame.image.load(os.path.join(path,filename)).convert_alpha()

