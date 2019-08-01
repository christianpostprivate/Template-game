import pygame as pg

import tilemaps
import sprites as spr
import utilities as utils

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
        self.map = tilemaps.Map(self.game, self.game.map_files[0])
        self.map.create_map()
        self.map.rect.topleft = (0, 0)
        
        self.camera = utils.Camera(self.game, self.map.size.x, self.map.size.y,
                                   'SLIDE')
        
        self.player = self.game.all_sprites.sprites()[0]
        
               
    def get_event(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                self.quit = True
                       
    
    def update(self, dt):
        if not self.camera.is_sliding:
            self.game.all_sprites.update(dt)
        self.camera.update(self.player)
              
        
    def draw(self, screen):
        screen.fill(pg.Color('black'))
        self.map.draw(screen, self.camera.apply_rect(self.map.rect))
        
        for sprite in self.game.all_sprites:
            self.game.screen.blit(sprite.image, self.camera.apply(sprite))
        
# =============================================================================
#         for s in self.game.all_sprites:
#             pg.draw.rect(screen, pg.Color('white'), self.camera.apply_rect(s.rect), 1)
# =============================================================================
        


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
        
        
        
        