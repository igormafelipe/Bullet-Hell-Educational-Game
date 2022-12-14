#!/usr/bin/env python3
# encoding: utf-8
"""
SpaceShip.py
"""

import sys, pygame, random
import constants, colors
from entities.SpaceShip import SpaceShip
from entities.Meteor import Meteor
from entities.Projectile import Projectile
import transitions
import os

cur_dir = os.path.abspath(".")
os.system(f"pip install --upgrade -r {cur_dir}/requirements.txt")

pygame.init()

display = pygame.display.set_mode(constants.SCREEN_SIZE, 
                                 pygame.WINDOWMAXIMIZED)
background_img = pygame.image.load("./images/backgrounds/bg.jpg").convert_alpha()
background = pygame.transform.smoothscale(background_img, display.get_size())
bg_center = background.get_rect().center

meteor_imgs = [pygame.image.load("./images/sprites/asteroids/asteroid_1.png").convert_alpha(),
               pygame.image.load("./images/sprites/asteroids/asteroid_2.png").convert_alpha(),
               pygame.image.load("./images/sprites/asteroids/asteroid_3.png").convert_alpha()]

font = pygame.font.Font(constants.TEXT_FONT, constants.TEXT_SIZE)

def GameComplete():
    game_complete_screen = pygame.image.load("./images/game_complete.jpg").convert()
    game_complete_screen = pygame.transform.smoothscale(game_complete_screen, 
                                                display.get_size())
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
    
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_SPACE]:
            Runner(constants.START_PHASE)
        if keys[pygame.K_ESCAPE]:
            sys.exit()
        
        display.fill(colors.BLACK)
        display.blit(game_complete_screen, constants.BACKGROUND_POSITION)
        pygame.display.flip()

def GameOver():
    game_over_screen = pygame.image.load("./images/backgrounds/gameover.jpg").convert()
    game_over_screen = pygame.transform.smoothscale(game_over_screen, 
                                                display.get_size())
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
    
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_SPACE]:
            Runner(constants.START_PHASE)
        if keys[pygame.K_ESCAPE]:
            sys.exit()
        
        display.fill(colors.BLACK)
        display.blit(game_over_screen, constants.BACKGROUND_POSITION)
        pygame.display.flip()

def CleanUp(meteors, spaceship):
    for meteor in meteors:
        del meteor
    del spaceship

def NextLevel(level):
    if level >= constants.PHASES:
        GameComplete()
    else:
        transitions.Transition(level, display)
        Runner(level + 1)

def Runner(level):
    transitions.LevelScreen(level, display)
    spaceship = SpaceShip(constants.SPACESHIP_SPEED, 
                          constants.SPACESHIP_INITIAL_POS)
    
    bullet_counter = font.render(f"Bullets: {spaceship.projectiles}/{constants.SPACESHIP_INITIAL_PROJECTILES}", 
                                 True, colors.WHITE, colors.BLACK)
    bullet_counter_rect = bullet_counter.get_rect()
    bullet_counter_rect.center = constants.BULLET_COUNTER_POSITION
    
    timer = font.render(f"Time: {constants.TIME_PER_LEVEL}", True, colors.WHITE, colors.BLACK)
    timer_rect = timer.get_rect()
    timer_rect.center = constants.TIMER_POSITION
    
    meteors = []
    num_meteors = 0

    orientation = Meteor.BOTTOM if level == constants.PHASES else Meteor.TOP

    clock = pygame.time.Clock()
    initial_time = pygame.time.get_ticks()
    projectiles = []
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            if (event.type == pygame.KEYDOWN 
                and event.key == pygame.K_LSHIFT
                and spaceship.projectiles > 0):
                spaceship.projectiles -= 1
                bullet_counter = font.render(f"Bullets: {spaceship.projectiles}/{constants.SPACESHIP_INITIAL_PROJECTILES}", 
                                             True, colors.WHITE, colors.BLACK)
                projectiles.append(Projectile(spaceship))
        
        #PHASE TRANSITION
        if pygame.time.get_ticks() - initial_time > constants.TIME_PER_LEVEL:
            CleanUp(meteors, spaceship)
            NextLevel(level)
            return
        
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            spaceship.move(up=True)
        if keys[pygame.K_DOWN]:
            spaceship.move(down=True)
        if keys[pygame.K_LEFT]:
            spaceship.move(left=True)
        if keys[pygame.K_RIGHT]:
            spaceship.move(right=True)
            
        spaceship.UpdateSprite()
        
        if num_meteors < constants.ASTEROIDS_PER_LEVEL[level]:
            num_meteors += 1
            m_img = meteor_imgs[random.randint(0, len(meteor_imgs) - 1)]
            meteors.append(Meteor(m_img, orientation))
        
        for meteor in meteors:
            meteor.move()
                
            if meteor.pos.colliderect(spaceship.pos):
                CleanUp(meteors, spaceship)
                GameOver()
            
            for projectile in projectiles:
                if meteor.pos.colliderect(projectile.pos):
                    temp = projectile
                    projectiles.remove(projectile)
                    del temp

                    m_img = meteor_imgs[random.randint(0, len(meteor_imgs) - 1)]
                    meteor.recycle(m_img)
                
                
        for projectile in projectiles:
            if projectile.pos.top <= 0:
                projectiles.remove(projectile)
                continue
            projectile.move()
        
        display.fill(colors.BLACK)
        display.blit(background, constants.BACKGROUND_POSITION)
        display.blit(spaceship.image, spaceship.pos)
        display.blit(bullet_counter, bullet_counter_rect)
        display.blit(timer, timer_rect)
        
        for meteor in meteors:
            display.blit(meteor.image, meteor.pos)
            
        for projectile in projectiles:
            display.blit(projectile.image, projectile.pos)
        
        pygame.display.flip()
        current_time = constants.TIME_PER_LEVEL - (pygame.time.get_ticks() - initial_time)
        current_time //= 1000
        timer = font.render(f"Time: {current_time}", True, colors.WHITE, colors.BLACK)
        clock.tick(30) #how many updates/frames per second?
        
Runner(constants.START_PHASE)