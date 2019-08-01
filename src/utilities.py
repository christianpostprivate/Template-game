import pygame as pg

import settings as st



vec = pg.math.Vector2



class Camera():
    '''
    modified from http://kidscancode.org/lessons/
    modes are
        FOLLOW: player is always in the middle of the screen
        PAN: camera pans as soon as the player leaves the screen
        SLIDE: like pan, but with a sliding animation
    '''
    def __init__(self, game, map_width, map_height, mode='FOLLOW'):
        self.game = game
        self.rect = pg.Rect(0, 0, map_width, map_height)
        self.map_width = map_width
        self.map_height = map_height
        self.mode = mode

        self.is_sliding = False
        self.target_pos = vec()
        self.prev_pos = vec()
        # previous quadrant
        self.prev_qw = 0
        self.prev_qh = 0
        
        self.slide_speed = 1 # pixel per frame, change this to dt


    def apply(self, entity):
        return entity.rect.move(self.rect.topleft)


    def apply_rect(self, rect):
        return rect.move(self.rect.topleft)


    def apply_point(self, point):
        return point - vec(self.rect.x, self.rect.y)


    def update(self, target):
        if self.mode == 'FOLLOW':
            x = -target.rect.x + self.game.screen_rect.w // 2
            y = -target.rect.y + self.game.screen_rect.h // 2
        elif self.mode == 'PAN':
            # divide into quadrants
            quads_w = self.rect.w // self.game.screen_rect.w
            quads_h = self.rect.h // self.game.screen_rect.h
            # which quadrant the target is in 
            # TODO: remove unnecessary calculations...
            qw = target.rect.x // (self.rect.w // quads_w)
            qh = target.rect.y // (self.rect.h // quads_h)
            
            x = (self.game.screen_rect.w) * -qw
            y = (self.game.screen_rect.h) * -qh 

            
            pg.display.set_caption(f'({x}/{y})')
        elif self.mode == 'SLIDE':
            # divide into quadrants
            quads_w = self.rect.w // self.game.screen_rect.w
            quads_h = self.rect.h // self.game.screen_rect.h
            # which quadrant the target is in 
            # TODO: remove unnecessary calculations...
            qw = target.rect.x // (self.rect.w // quads_w)
            qh = target.rect.y // (self.rect.h // quads_h)
            
            self.target_pos.x = (self.game.screen_rect.w) * -qw
            self.target_pos.y = (self.game.screen_rect.h) * -qh
            
            #print(qw, self.prev_qw)
            if qw != self.prev_qw or qh != self.prev_qh:
                #self.is_sliding = True
                
                # calculate the sliding direction
                dirx = qw - self.prev_qw
                diry = qh - self.prev_qh
                
                x = self.prev_pos.x - self.target_pos.x
                y = self.prev_pos.y - self.target_pos.y
                
                pg.display.set_caption(f'({self.prev_pos.x}/{self.target_pos.x})')
            else:
    
                x = self.target_pos.x
                y = self.target_pos.y
                
                self.prev_pos.x = self.target_pos.x
                self.prev_pos.y = self.target_pos.y

            self.prev_qw = qw
            self.prev_qh = qh
            

        # limit scrolling to map size
        x = min(0, x) # left
        x = max(-(self.map_width - st.SCREEN_W), x) # right
        y = min(0, y) # top
        y = max(-(self.map_height - st.SCREEN_H), y) # bottom
        
        self.rect = pg.Rect(x, y, self.map_width, self.map_height)