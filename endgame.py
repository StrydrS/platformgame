import pygame
from game_data import levels
from support import import_folder
from decoration import Sky

       
class Endgame:
    def __init__(self, surface, coin_amount, max_level):
        self.display_surface = surface
        self.coin_amount = coin_amount
        self.max_level = max_level
    
    
              
    def run(self):
    
        self.sky.draw(self.display_surface)
        self.draw_paths()
        self.icon.update()
        self.nodes.draw(self.display_surface)
        self.icon.draw(self.display_surface)