## Project: pyEnkido
## Module: controller
## Author: Salwan

import pyenkido.entity

class Controller(object):
    def __init__(self, entity = pyenkido.entity.Entity()):
        self.attached_to_entity(entity)
        self.entity.attached_to_controller(self)
        self.active = False

    def update(self):
        pass

    def activate(self):
        self.active = True

    def deactivate(self):
        self.active = False

    def attached_to_entity(self, entity):
        self.entity = entity

    def detached_from_entity(self):
        self.entity = None

    def game_paused(self):
        pass

    def game_resumed(self):
        pass

    def key_down(self, key):
        pass

    def key_up(self, key):
        pass

    def mouse_key_down(self, event):
        pass

    def mouse_key_up(self, event):
        pass

    def mouse_move(self, event):
        pass
