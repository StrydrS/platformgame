import pygame, sys
from settings import *
from tiles import Tile
from level import Level
from game_data import level_0

pygame.init()
sWIDTH = WIDTH
sHEIGHT = HEIGHT

screen = pygame.display.set_mode((sWIDTH, sHEIGHT))
clock = pygame.time.Clock()

level = Level(level_0, screen)


while True: 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    #background
    screen.fill('grey')
    level.run() 
    
    pygame.display.update()
    clock.tick(60)