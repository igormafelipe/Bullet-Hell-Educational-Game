#!/usr/bin/env python
# encoding: utf-8
"""
Meteor.py
"""

import constants, pygame, sys, colors
import random

class Meteor:
    TOP = 1
    BOTTOM = 2
    ROTATION_ANGLE_INCREASE = 1
     
    used_positions = set()
    
    def __init__(self, image, orientation):
        self.angle = 0
        self.orientation = orientation
        self.recycle(image)
    
    def __del__(self):
        if self.pos.right in Meteor.used_positions:
            Meteor.used_positions.remove(self.pos.right)
    
    def recycle(self, image):
        i = random.randint(0, 2)
        
        self.speed = constants.METEOR_SPEED[i]
        self.size = constants.METEOR_SIZES[i] * constants.METEOR_SIZE_MULTIPLIER
        self.collision_size = self.size - constants.METEOR_SIZES[i] * 2
        
        
        sprite_size = self.size, self.size
        image = pygame.transform.smoothscale(image, sprite_size)
        image = image.convert_alpha()
        image.set_colorkey(colors.BLACK)
        
        if self.orientation == self.TOP:
            y_pos = 0 - (self.size * 2)
        elif self.orientation == self.BOTTOM:
            y_pos = constants.SCREEN_HEIGHT + (self.size * 2)
        else:
            print("In Recycle: Meteor orientation messed up. Defaulting to TOP")
            y_pos = 0
                
        x_pos = random.randint(self.size, constants.SCREEN_WIDTH)
        if x_pos in Meteor.used_positions:
            x_pos += self.size + 10
        
        Meteor.used_positions.add(x_pos)
        # print(Meteor.used_positions)
        
        self.image = image
        self.original_image = image
        self.pos = pygame.Rect(x_pos, y_pos, self.collision_size, self.collision_size)
        
    
    def rotate(self):
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.image.set_colorkey(colors.BLACK)
        self.angle = (self.angle + self.ROTATION_ANGLE_INCREASE) % 360
        
    def move(self):
        self.rotate()       
        if self.orientation == self.TOP:
            if (self.pos.top > constants.METEOR_SIZE_MULTIPLIER * 4 and 
                self.pos.right in Meteor.used_positions):
                Meteor.used_positions.remove(self.pos.right)
                
            if self.pos.top > constants.SCREEN_HEIGHT:
                self.recycle(self.original_image)
            self.pos.top += self.speed
        elif self.orientation == self.BOTTOM:
            #keeps track of meteor's x axis position to desincourage same spawns.
            if (self.pos.top > constants.SCREEN_HEIGHT - (constants.METEOR_SIZE_MULTIPLIER * 4) 
                and self.pos.right in Meteor.used_positions):
                Meteor.used_positions.remove(self.pos.right)
                
            if self.pos.top <= 0:
                self.recycle(self.original_image)
            self.pos.top -= self.speed