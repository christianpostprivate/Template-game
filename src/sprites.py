import pygame as pg
#from random import randint

import settings as st


vec = pg.math.Vector2

RIGHT = 2 #TODO: come up with a better system
DOWN = 8
LEFT = 6
UP = 9


# TODO: make seperate parent classes for Sprite and animated sprite

class State():
    ''' base class for player/NPC state machine '''
    def __init__(self, game, sprite):
        self.game = game
        self.sprite = sprite # the sprite object this state belongs to
        self.next = None # what comes after if this is done
        self.done = False # if true, the next state gets executed
        self.previous = None # the state that was executed before
        self.name = self.sprite.state_name
        
        # get the image list for this state
        self.images = [image.copy() for image in self.sprite.image_dict[self.name]]
        
    def startup(self):
        self.sprite.image = self.images[0].copy()
        self.sprite.rect = self.sprite.image.get_rect()
        self.sprite.rect.topleft = self.sprite.pos # only works when images are of the same size
    
    def cleanup(self):
        print(f'cleaning up {self.name}')
        pass
    
    def update(self, dt):
        pass

    
    

class Animated_sprite(pg.sprite.Sprite):
    ''' sprite class with a list of images that animate'''
    def __init__(self, game, images, **kwargs):
        self.game = game
        super().__init__(game.all_sprites)
        for key, value in kwargs.items():
            setattr(self, key, value)
        # set additional custom properties (from Tiled 'properties' dict)
        if hasattr(self, 'properties'):
            for key, value in self.properties.items():
                setattr(self, key, value)
                
        try:
            # try accessing to width and height
            # if this fails, take the default tile size
            self.size = (self.width, self.height)
        except AttributeError:
            self.width = st.TILE_W
            self.height = st.TILE_H
            self.size = (st.TILE_W, st.TILE_H)
        self.pos = (self.x, self.y)
        
        self.image_dict = images

    
    def flip_state(self):
        '''set the state to the next if the current state is done'''
        self.state.done = False
        # set the current and next state to the previous and current state
        previous, self.state_name = self.state_name, self.state.next
        self.state.cleanup()
        self.state = self.state_dict[self.state_name](self)
        self.state.startup()
        self.state.previous = previous
        
    
    def update(self, dt):
        if self.state.done:
            self.flip_state()
        self.state.update(dt)
    
    
    def animate(self, dt):
        # loop through all of self.images and set self.image to the next
        # image if the time exceeds the delay
        self.anim_timer += dt
        if self.anim_timer >= self.anim_delay:
            # reset the timer
            self.anim_timer = 0
            # advance the frame
            self.anim_frame = (self.anim_frame + 1) % len(self.state.images)
            # set the image and adjust the rect
            self.image = self.state.images[self.anim_frame]
            self.rect = self.image.get_rect()
            self.rect.topleft = self.pos



class Test_sprite(Animated_sprite):
    ''' basic sprite class for testing '''
    def __init__(self, game, **kwargs):
        images = {'Default_state': game.graphics['knight_images']}
        
        super().__init__(game, images, **kwargs)
        
        self.acc = vec()
        self.vel = vec()
        self.speed = 1000
        self.friction = 0.7
        
        # setup state machine
        self.state_dict = {
                'Default_state': self.Default_state,
                'Test_state': self.Test_state
                }
        self.state_name = 'Default_state'
        self.state = self.state_dict[self.state_name](self)
        self.state.startup()
    
    
    class Default_state(State):
        ''' this is the default state for this class '''
        def __init__(self, sprite):
            super().__init__(sprite.game, sprite)
            self.next = 'Test_state'
            
            self.lastdir = DOWN
        
        
        def startup(self):
            super().startup()
            
            self.sprite.anim_timer = 0 # time in seconds
            self.sprite.anim_delay = 0.2 # animation delay in seconds
            self.sprite.anim_frame = 0 # current index of the images list
            
        
        def update(self, dt):
            keys = pg.key.get_pressed()

            self.sprite.acc *= 0
            self.sprite.acc.x = keys[pg.K_d] - keys[pg.K_a]
            self.sprite.acc.y = keys[pg.K_s] - keys[pg.K_w]
            if self.sprite.acc.length() > 1:
                self.sprite.acc.scale_to_length(1)
            self.sprite.vel += self.sprite.acc * self.sprite.speed * dt
            self.sprite.vel *= self.sprite.friction
            self.sprite.pos += self.sprite.vel * dt
            self.sprite.rect.topleft = self.sprite.pos
            
            if self.sprite.vel.length() < 10:
                self.sprite.vel *= 0
                images = self.sprite.image_dict[self.name]
                self.images = [images[self.lastdir]] # TODO: select the idle images
            else:
                images = self.sprite.image_dict[self.name]
                if self.sprite.acc.x > 0:
                    self.images = images[2:4]
                    self.lastdir = RIGHT
                elif self.sprite.acc.x < 0:
                    self.images = images[6:8]
                    self.lastdir = LEFT
                if self.sprite.acc.y > 0:
                    self.images = images[0:2]
                    self.lastdir = DOWN
                elif self.sprite.acc.y < 0:
                    self.images = images[4:6]
                    self.lastdir = UP
            
            self.sprite.animate(dt)
            
    
    class Test_state(State):
        ''' for testing '''
        def __init__(self, sprite):
            super().__init__(sprite.game, sprite)
            self.next = 'Default_state'
        
        
        def startup(self):
            super().startup()
            
            self.sprite.anim_timer = 0 # time in seconds
            self.sprite.anim_delay = 0.5 # animation delay in seconds
            self.sprite.anim_frame = 0 # current index of the images list
            
        
        def update(self, dt):
            self.sprite.animate(dt)
            
            keys = pg.key.get_pressed()
# =============================================================================
#             if not keys[pg.K_r]:
#                 self.done = True
# =============================================================================
            
    
    def update(self, dt):
        super().update(dt)
    





