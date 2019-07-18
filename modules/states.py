import pygame as pg
from random import randint

from modules import tilemaps
from modules import sprites as spr

'''
Based on the state machine tutorial by metulburr
https://python-forum.io/Thread-PyGame-Creating-a-state-machine
'''


class State(object):
    '''parent class for all states'''
    def __init__(self, game):
        self.game = game
        self.next = None # what comes after if this is done
        self.done = False # if true, the next state gets executed
        self.quit = False # if true, the game application is terminated
        self.previous = None # the state that was executed before
    
    def startup(self):
        pass
    
    def cleanup(self):
        pass
    
    def get_event(self, event):
        pass
    


class In_game(State):
    def __init__(self, game):
        State.__init__(self, game)
    
    
    def startup(self):
        # for testing, delete later
        self.map = tilemaps.Map(self.game, 'data/tilemaps/sample_map.tmx')
        self.map.create_map()
        
        images = {'Default_state': [pg.Surface((16, 16)) for _ in range(12)],
                  'Test_state': [pg.Surface((16, 16)) for _ in range(12)]}
        for img in images['Default_state']:
            img.fill((0, randint(100, 255), randint(100, 255)))
        for img in images['Test_state']:
            img.fill((randint(100, 255), randint(100, 255), 0))
        self.s = spr.Animated_sprite(game=self.game, images=images, x=16, y=16)
        
               
    def get_event(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                self.quit = True
                       
    
    def update(self, dt):
        self.game.all_sprites.update(dt)
              
        
    def draw(self, screen):
        screen.fill(pg.Color('blue'))
        
        self.map.draw(screen, (0, 0))
        
        self.game.all_sprites.draw(screen)
        


class Title_screen(State):
    def __init__(self, game):
        State.__init__(self, game)
        self.next = 'In_game'

        
    def get_event(self, event):
        # press any key to continue
        if event.type == pg.KEYDOWN:
            self.done = True
                       
    
    def update(self, dt):
        pass
              
        
    def draw(self, screen):
        screen.fill(pg.Color('red'))
        txt = 'Template game. Press any key to start.'
        txt_surf = self.game.fonts['default'].render(txt, False, pg.Color('white'))
        txt_rect = txt_surf.get_rect()
        txt_rect.center = self.game.screen_rect.center
        screen.blit(txt_surf, txt_rect)
        
        
        
        