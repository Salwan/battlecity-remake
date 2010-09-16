## Project: pyEnkido
## Module: particle system
## Author: Salwan

import pygame
import random

class ParticleSystem(object):
    def __init__(self, position, time_step, total_particles, particle_color_list):
        self.alive = True
        self.position = position
        self.timeStep = time_step
        self.maxParticles = 10
        self.particleLife = 60
        self.spawnEvery = 1
        self.spawnTicks = 0
        self.totalParticles = total_particles
        self.particleColorList = particle_color_list
        # Format of each particle tuple: (alive, position, velocity, life, type)
        self.particles = []
        for i in range(0, self.maxParticles):
            self.particles.append((False, (0.0, 0.0), (0.0, 0.0), 0, 0))

    def update(self):
        self.spawnTicks += 1        
        if self.totalParticles <= 0:
            still_alive = False
            for i in range(0, self.maxParticles):
                if self.particles[i][0]:
                    still_alive = True
                    break
            if not still_alive:
                self.kill()
        for i in range(0, self.maxParticles):
            if self.spawnTicks >= self.spawnEvery and not self.particles[i][0] and self.totalParticles > 0:
                rx = (random.random() * 50.0) - 25.0
                ry = (random.random() * 50.0) - 25.0
                fp = (float(self.position[0]), float(self.position[1]))
                self.particles[i] = (True, fp, (rx, ry), self.particleLife, 0)
                self.totalParticles -= 1
                break
            else:
                l = self.particles[i][3] - 1
                if l <= 0:
                    self.particles[i] = (False, (0.0, 0.0), (0.0, 0.0), 0, 0)
                else:
                    p = self.particles[i][1]
                    v = self.particles[i][2]
                    p = (p[0] + v[0] * self.timeStep, p[1] + v[1] * self.timeStep)
                    self.particles[i] = (True, p, v, l, 0)

    def preDraw(self, screen):
        pass

    def draw(self, screen):
        for i in range(0, self.maxParticles):
            if self.particles[i][0]:
                p = (int(self.particles[i][1][0]), int(self.particles[i][1][1]))
                screen.set_at(p, random.choice(self.particleColorList))

    def postDraw(self, screen):
        pass

    def setPosition(self, new_pos):
        self.position = new_pos

    def getPosition(self):
        return self.position

    def spawned(self):
        pass

    def killed(self):
        pass

    def kill(self):
        self.killed()
        self.alive = False

    def isAlive(self):
        return self.alive

