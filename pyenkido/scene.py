## Project: pyEnkido
## Module: scene
## Author: Salwan

import pygame
import pyenkido.gui.gui_manager
import pyenkido.entity
import pyenkido.controller

class Scene(object):
    def __init__(self, scenemanager, screen):
        self.screen = screen
        self.sceneMgr = scenemanager
        self.guiMgr = pyenkido.gui.gui_manager.GUIManager(self.screen)
        self.controllers = []
        self.particleSystems = []
        self.isPaused = False

    def _base_start(self):
        self.guiMgr = pyenkido.gui.gui_manager.GUIManager(self.screen)
        self.controllers = []
        self.start()
        
    def start(self):
        pass
    
    def update(self):
        self.updateControllers()
        self.updateEntities()
        self.updateParticles()
   
    def draw(self):
        self.drawParticles()

    def spawnParticleSystem(self, particle_sys):
        self.particleSystems.append(particle_sys)

    def updateControllers(self):
        if len(self.controllers) > 0:
            to_remove = []
            for c in self.controllers:
                c.update()
                if c.entity and not c.entity.isAlive():
                    to_remove.append(c)
            if len(to_remove) > 0:
                for t in to_remove:
                    self.removeController(t)

    def updateEntities(self):
        pass

    def updateParticles(self):
        to_remove = []
        for p in self.particleSystems:
            if p.isAlive():
                p.update()
            else:
                to_remove.append(p)
        if len(to_remove) > 0:
            for t in to_remove:
                self.particleSystems.remove(t)

    def drawParticles(self):
        for p in self.particleSystems:
            if p.isAlive():
                p.draw(self.screen)

    def attachControllerToEntity(self, controller, entity):
        controller.attached_to_entity(entity)
        entity.attached_to_controller(controller)
        self.controllers.append(controller)

    def removeController(self, controller):
        if controller.entity:
            controller.entity.detached_from_controller()
        controller.detached_from_entity()
        self.controllers.remove(controller)

    def _controller_key_down(self, key):
        if self.isPaused:
            return
        for c in self.controllers:
            c.key_down(key)

    def _controller_key_up(self, key):
        if self.isPaused:
            return
        for c in self.controllers:
            c.key_up(key)

    def _controller_mouse_key_down(self, event):
        if self.isPaused:
            return
        for c in self.controllers:
            c.mouse_key_down(event)

    def _controller_mouse_key_up(self, event):
        if self.isPaused:
            return
        for c in self.controllers:
            c.mouse_key_up(event)

    def _controller_mouse_move(self, event):
        if self.isPaused:
            return
        for c in self.controllers:
            c.mouse_move(event)
        
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
        
    def end(self):
        pass
        