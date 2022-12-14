#!/usr/bin/env python
# encoding: utf-8
"""
Projectile.py
"""

import constants, pygame, colors

class Projectile:
    def __init__(self, spaceship):
        self.initial_position = spaceship.pos
        self.image = pygame.image.load("./images/sprites/projectiles/projectile.png").convert_alpha()
        self.image = pygame.transform.smoothscale(self.image, constants.PROJECTILE_SIZE)
        self.image.set_colorkey(colors.BLACK)
        self.pos = pygame.Rect(spaceship.pos.midtop, constants.PROJECTILE_SIZE)
    
    def move(self):
        if (self.pos.top <= 0):
            del self
        else:
            self.pos.top -= constants.PROJECTILE_SPEED
        