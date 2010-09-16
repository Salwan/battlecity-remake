## Project: pyEnkido
## Module: scene manager
## Author: Salwan

import scene
import pygame

class SceneManager:
    def __init__(self, screen, screen_effects_manager):
        self.screen = screen
        self.scenes = {}
        self.screenEffectsMgr = screen_effects_manager
        self.default_scene = scene.Scene(self, self.screen)
        self.active_scene = self.default_scene
        self.requests = []
        self.gamedb = {}
        self.sounds = []
        self.endGame = False
        
    def get_game_db(self):
        return self.gamedb
    
    def clear_game_db(self):
        self.gamedb = {}
        
    def play_until_finish(self, sound, loops=0, maxtime=0, fade_ms=0):
        self.sounds.append(sound.play(loops, maxtime, fade_ms))
        
    def update_sounds(self):
        to_be_removed = []
        for s in self.sounds:
            if not s.get_busy():
                to_be_removed.append(s)
        for s in to_be_removed:
            self.sounds.remove(s)
        
    def has_scene(self, id):
        return self.scenes.has_key(id)
        
    def add_scene(self, id, scene):
        if self.has_scene(id):
            print "SceneManager: Adding scene failed because scene already exists!"
        self.scenes[id] = scene
        
    def remove_scene(self, id):
        print "SceneManager: REMOVED SCENE", id
        del self.scenes[id]
        
    def change_scene(self, id, end_scene = True):
        if self.has_scene(id):
            self.requests.append(['change', id, end_scene])
        else:
            print "SceneManager: Request 'change' failed, scene",id,"does not exist."
            raise 'fatal'
        
    def update(self):
        self.active_scene.update()
        self.active_scene.guiMgr.update()
        self.update_sounds()
        self.process_requests()
        
    def draw(self):
        self.active_scene.draw()
        # GUI draws here
        self.active_scene.guiMgr.draw()
        
    def key_down(self, key):
        self.active_scene._controller_key_down(key)
        self.active_scene.guiMgr.key_down(key)
        self.active_scene.key_down(key)
        
    def key_up(self, key):
        self.active_scene._controller_key_up(key)
        self.active_scene.guiMgr.key_up(key)
        self.active_scene.key_up(key)
        
    def mouse_key_down(self, event):
        self.active_scene._controller_mouse_key_down(event)
        self.active_scene.guiMgr.mouse_key_down(event)
        self.active_scene.mouse_key_down(event)
        
    def mouse_key_up(self, event):
        self.active_scene._controller_mouse_key_up(event)
        self.active_scene.guiMgr.mouse_key_up(event)
        self.active_scene.mouse_key_up(event)
        
    def mouse_move(self, event):
        self.active_scene._controller_mouse_move(event)
        self.active_scene.guiMgr.mouse_move(event)
        self.active_scene.mouse_move(event)
        
    def add_screen_effect(self, effect):
        self.screenEffectsMgr.add_effect(effect)
        
    def clear_screen_effects(self):
        self.screenEffectsMgr.clear()
        
    def process_requests(self):
        for r in self.requests:
            if r[0] == 'change':
                if r[2]:
                    self.active_scene.end()
                self.active_scene = self.scenes[r[1]]
                print self.active_scene, r
                self.active_scene._base_start()
            elif r[0] == 'endgame':
                self.endGame = True
        self.requests = []

    def closeGame(self):
        self.requests.append(('endgame', 0))

    def stopAllSounds(self):
        pygame.mixer.stop()