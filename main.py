import pygame, sys
from settings import *
from level import Level
from overworld import Overworld
from ui import UI


class Game:
    def __init__(self):
        
        #game attributes
        self.max_level = 0 
        self.max_health = 100
        self.current_health = 100
        self.coins = 0
        
        #audio
        self.level_bg_music = pygame.mixer.Sound('audio/level_music.wav')
        self.level_bg_music.set_volume(0.05)
        self.overworld_bg_music = pygame.mixer.Sound('audio/overworld_music.wav')
        self.overworld_bg_music.set_volume(0.05)
        
        
        #overworld creation
        self.overworld = Overworld(0, self.max_level, screen, self.create_level)
        self.gamestate = 'overworld'
        self.overworld_bg_music.play(loops = -1)
        
        #ui creation
        self.ui = UI(screen)
        
      
        
    def create_level(self, current_level):
        self.level = Level(current_level, screen, self.create_overworld, self.change_coins, self.change_health)
        self.gamestate = 'level'
        self.overworld_bg_music.stop()
        self.level_bg_music.play(loops = -1)
        
    def create_overworld(self, current_level, new_max_level):
        if new_max_level > self.max_level:
            self.max_level = new_max_level
        self.level_bg_music.stop()    
        self.overworld = Overworld(current_level, self.max_level, screen, self.create_level)
        self.gamestate = 'overworld'
        self.overworld_bg_music.play(loops = -1)

    def change_coins(self, amount):
        self.coins += amount
    
    def change_health(self, amount):
        self.current_health += amount
    
    def check_game_over(self):
        if self.current_health <= 0:
            self.current_health = 100
            self.coins = 0
            self.max_level = 0
            
            self.overworld = Overworld(0, self.max_level, screen, self.create_level)
            self.gamestate = 'overworld'
            
    def run(self): 
        if self.gamestate == 'overworld':
            self.overworld.run()
        else: 
            self.level.run()
            self.ui.show_health(self.current_health,self.max_health)
            self.ui.show_coins(self.coins)
            self.check_game_over()       
            
            
pygame.init()
sWIDTH = WIDTH
sHEIGHT = HEIGHT

screen = pygame.display.set_mode((sWIDTH, sHEIGHT))
clock = pygame.time.Clock()
game = Game()

while True: 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    #background
    screen.fill('grey')
    game.run() 
    
    pygame.display.update()
    clock.tick(60)