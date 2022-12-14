#!/usr/bin/env python
# encoding: utf-8
"""
SpaceShip.py
"""
import constants, pygame, colors

class SpaceShip:
    spaceship_frames = ["./images/sprites/spaceship/space_ship_1.png",
                        "./images/sprites/spaceship/space_ship_2.png",
                        "./images/sprites/spaceship/space_ship_3.png"]
        
        
    frame = 0
    
    def __init__(self, speed, initial_pos):
        self.speed = speed
        self.UpdateSprite()
        self.projectiles = constants.SPACESHIP_INITIAL_PROJECTILES
        self.pos = pygame.Rect(initial_pos, constants.SPACESHIP_COLLISION)
        
        
    def UpdateSprite(self):
        image = pygame.image.load(self.spaceship_frames[self.frame]).convert_alpha()
        image = image.convert()
        image = pygame.transform.smoothscale(image, constants.SPACESHIP_SIZE)
        image.set_colorkey(colors.BLACK)
        self.frame = (self.frame + 1) % 3
        self.image = image
    
    def move(self, right = False, left = False, up = False, down = False):
        if right and self.pos.right < constants.SCREEN_WIDTH + constants.SPACESHIP_WIDTH//2:
            self.pos.right += self.speed
        if left and self.pos.right > 0 + constants.SPACESHIP_WIDTH - constants.SPACESHIP_WIDTH//2:
            self.pos.right -= self.speed
        if up and self.pos.top > 0 - constants.SPACESHIP_HEIGHT//2:
            self.pos.top -= self.speed
        if down and self.pos.top < constants.SCREEN_HEIGHT - \
                                   constants.SPACESHIP_HEIGHT + constants.SPACESHIP_HEIGHT//2:
            self.pos.top += self.speed