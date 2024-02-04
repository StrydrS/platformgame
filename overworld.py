import pygame
from game_data import levels
from support import import_folder
from decoration import Sky

class Node(pygame.sprite.Sprite):
    def __init__(self, pos, status, icon_speed, path):
        super().__init__()
        self.image = pygame.Surface((100,80))
        self.frames = import_folder(path)
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        
        if status == 'available':
            self.status = 'available'
        else:
            self.status = 'locked'
        self.rect = self.image.get_rect(center = pos)
        
        self.detection_zone = pygame.Rect(self.rect.centerx - (icon_speed/2),self.rect.centery - (icon_speed/2), icon_speed,icon_speed)

    def animate(self):
        self.frame_index += 0.15
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]
        
    def update(self):
        if self.status == 'available':
            self.animate()
            
        else: 
            tint_surface = self.image.copy()
            tint_surface.fill('black', None, pygame.BLEND_RGB_MULT)
            self.image.blit(tint_surface,(0,0))
        
class Icon(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.pos = pos
        self.image = pygame.Surface((20, 20))
        self.image = pygame.image.load('graphics/overworld/hat.png').convert_alpha()
        self.rect = self.image.get_rect(center = pos)
        
    def update(self):
        self.rect.center = self.pos
       
class Overworld:
    def __init__(self, start_level, max_level, surface, create_level, max_coins): 
        
        #setup
        self.display_surface = surface
        self.max_level = max_level
        self.current_level = start_level
        
        self.create_level = create_level
        
        self.max_coins = max_coins 
        
        #coin ui
        self.coin = pygame.image.load('graphics/ui/coin.png').convert_alpha()
        self.coin_rect = self.coin.get_rect(topleft = (950,61))
        self.font = pygame.font.Font('graphics/ui/ARCADEPI.TTF', 30)
        
        #movement logic
        self.moving = False
        self.move_direction = pygame.math.Vector2(0,0)
        self.speed = 8
        
        #sprites 
        self.setup_nodes()
        self.setup_icon()
        self.sky = Sky(8, 'overworld')
        
        #time 
        self.start_time = pygame.time.get_ticks()
        self.allow_input = False
        self.timer_len = 300
        
    def setup_nodes(self):
        self.nodes = pygame.sprite.Group()
        
        for index, node_data in enumerate(levels.values()):
            if index <= self.max_level:
                node_sprite = Node(tuple(node_data['node_pos']), 'available', self.speed,node_data['node_graphics'])
            else:
                node_sprite = Node(tuple(node_data['node_pos']),'locked', self.speed,node_data['node_graphics'])
            self.nodes.add(node_sprite)
            
            
    def show_coins(self,amount):
        self.display_surface.blit(self.coin, self.coin_rect)
        self.coin_num = self.font.render(str(amount) + " collected.", False, '#33323d')
        self.coin_num_rect = self.coin_num.get_rect(midleft = (self.coin_rect.right + 4, self.coin_rect.centery))
        self.display_surface.blit(self.coin_num, self.coin_num_rect)
    
    def setup_icon(self):
        self.icon = pygame.sprite.GroupSingle()
        icon_sprite = Icon(self.nodes.sprites()[self.current_level].rect.center)
        self.icon.add(icon_sprite)
    
    def draw_paths(self):
        if self.max_level > 0:
            points = [tuple(node['node_pos']) for index, node in enumerate(levels.values()) if index <= self.max_level]
            pygame.draw.lines(self.display_surface, 'red', False, points, 6)
    
    def input(self):
        keys = pygame.key.get_pressed()
        if not self.moving and self.allow_input:
            if keys[pygame.K_d] and self.current_level < self.max_level:
                self.move_direction = self.get_movement_data('next')
                self.current_level += 1
                self.moving = True
            elif keys[pygame.K_a] and self.current_level > 0:
                self.move_direction = self.get_movement_data('previous')
                self.current_level -= 1
                self.moving = True
            elif keys[pygame.K_SPACE]:
                self.create_level(self.current_level)
            
    
    
    def get_movement_data(self, target):
        start = pygame.math.Vector2(self.nodes.sprites()[self.current_level].rect.center)
        
        if target == 'next':  
            end = pygame.math.Vector2(self.nodes.sprites()[self.current_level + 1].rect.center)
        else: 
            end = pygame.math.Vector2(self.nodes.sprites()[self.current_level - 1].rect.center)
        
        return (end - start).normalize()
    
    def update_icon_pos(self):
        if self.moving and self.move_direction:
            self.icon.sprite.pos += self.move_direction * self.speed
            target_node = self.nodes.sprites()[self.current_level]
            if target_node.detection_zone.collidepoint(self.icon.sprite.pos):
                self.moving = False
                self.move_direction = pygame.math.Vector2(0,0)
                
    def input_timer(self):
        if not self.allow_input:
            current_time = pygame.time.get_ticks()
            if current_time - self.start_time >= self.timer_len:
                self.allow_input = True
              
    def run(self):
        self.input_timer()
        self.input()
        self.update_icon_pos()
        self.icon.update()
        self.nodes.update()
        
        
        self.sky.draw(self.display_surface)
        self.draw_paths()
        self.icon.update()
        self.nodes.draw(self.display_surface)
        self.icon.draw(self.display_surface)
        self.show_coins(self.max_coins)
    