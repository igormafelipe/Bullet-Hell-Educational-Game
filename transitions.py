
#!/bin/python3
# encoding: utf-8
"""
Transitions.py
"""

import pygame
import colors, constants
import sys

transition_screens = ["./images/backgrounds/lvl1_trans_screen.jpg", #dwarf
                      "./images/backgrounds/lvl2_trans_screen.jpg", #red giants
                      "./images/backgrounds/lvl3_trans_screen.jpg", #super nova
                      "./images/backgrounds/game_complete.jpg"] # Game complete

level_screens = ["./images/backgrounds/initial_screen.jpg",
                 "./images/backgrounds/phase_1.jpg",
                 "./images/backgrounds/phase_2.jpg",
                 "./images/backgrounds/phase_3.jpg"]

def Transition(curr_level, display):
    curr_trans_screen = pygame.image.load(transition_screens[curr_level])
    curr_trans_screen = pygame.transform.smoothscale(curr_trans_screen, 
                                                            display.get_size())
    
    #This is so one space press does not count for multiple screens
    pygame.time.wait(100)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
    
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_SPACE]:
            return
        
        if keys[pygame.K_ESCAPE]:
            sys.exit()
        
        display.fill(colors.BLACK)
        display.blit(curr_trans_screen, constants.BACKGROUND_POSITION)
        pygame.display.flip()
        

def LevelScreen(curr_level, display):
    curr_level_screen = pygame.image.load(level_screens[curr_level])
    curr_level_screen = pygame.transform.smoothscale(curr_level_screen, 
                                                            display.get_size())
    
    #This is so one space press does not count for multiple screens
    pygame.time.wait(100)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
    
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_SPACE]:
            return
        
        if keys[pygame.K_ESCAPE]:
            sys.exit()
        
        display.fill(colors.BLACK)
        display.blit(curr_level_screen, constants.BACKGROUND_POSITION)
        pygame.display.flip()