import pygame as pg
import json

import settings as st



vec = pg.math.Vector2


def difference(list1, list2):
    return [1 if elem and not list1[i] else 0 for i, elem in enumerate(list2)]


def is_jsonable(x):
    try:
        json.dumps(x)
        return True
    except:
        return False


class Camera():
    '''
    modified from http://kidscancode.org/lessons/
    modes are
        FOLLOW: player is always in the middle of the screen
        CUT: camera pans as soon as the player leaves the screen
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
        
        self.slide_speed = 0.05 # percent, change this to dt
        self.slide_amount = 0


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
        elif self.mode == 'CUT':
            # divide into quadrants
            quads_w = self.rect.w // self.game.screen_rect.w
            quads_h = self.rect.h // self.game.screen_rect.h
            # which quadrant the target is in.
            qw = target.rect.x // (self.rect.w // quads_w)
            qh = target.rect.y // (self.rect.h // quads_h)
            
            x = (self.game.screen_rect.w) * qw * -1
            y = (self.game.screen_rect.h) * qh * -1
            
        elif self.mode == 'SLIDE':
            # divide into quadrants
            quads_w = self.rect.w // self.game.screen_rect.w
            quads_h = self.rect.h // self.game.screen_rect.h
            # which quadrant the target is in 
            qw = target.rect.x // (self.rect.w // quads_w)
            qh = target.rect.y // (self.rect.h // quads_h)
            
            # limit the quadrants to the map
            #qw = qw % quads_w # not a good idea when player.pos isn't wrapping
            qw = min(max(qw, 0), quads_w - 1)
            qh = min(max(qh, 0), quads_h - 1)
            
            
            self.target_pos.x = (self.game.screen_rect.w) * qw * -1
            self.target_pos.y = (self.game.screen_rect.h) * qh * -1

            if qw != self.prev_qw or qh != self.prev_qh:
                self.is_sliding = True
                
                self.slide_amount += self.slide_speed
                self.slide_amount = min(self.slide_amount, 1)
                between = self.prev_pos.lerp(self.target_pos, self.slide_amount)
                
                x = int(between.x)
                y = int(between.y)
                
                if self.target_pos.x == x and self.target_pos.y == y:
                    self.prev_qw = qw
                    self.prev_qh = qh
                    self.slide_amount = 0
                
            else:
                self.is_sliding = False
                
                x = self.target_pos.x
                y = self.target_pos.y
                
                self.prev_pos.x = self.target_pos.x
                self.prev_pos.y = self.target_pos.y

                self.prev_qw = qw
                self.prev_qh = qh

            #pg.display.set_caption(f'({qw}/{qh})')

        # limit scrolling to map size
        x = min(0, x) # left
        x = max(-(self.map_width - st.SCREEN_W), x) # right
        y = min(0, y) # top
        y = max(-(self.map_height - st.SCREEN_H), y) # bottom
        
        self.rect = pg.Rect(x, y, self.map_width, self.map_height)