## Project: pyEnkido
## Module: Tile
## Author: Salwan

import os, pygame
import pyenkido.entity 

class Tile(pyenkido.entity.Entity):
    def __init__(self, group, image, rect, type, layer = 0):
        super(Tile, self).__init__()
        self.layer = layer
        self.type = type
        if group != None:
            group.add(self)
        self.image = image
        self.rect = rect
    
    def update(self):
        pass

    def save(self, path, filename):
        #file = open(os.path.join(path, filename), "w")
        #file.close()
        pass

    def load(self, path, filename):
        #file = open(os.path.join(path, filename), "rb")
        #file.close()
        pass
