import pygame as pg

from modules import settings as st


# TODO: make seperate parent classes for Sprite and animated sprite



class Test_sprite(pg.sprite.Sprite):
    ''' basic sprite class for testing '''
    def __init__(self, game, **kwargs):
        self.game = game
        super().__init__(game.all_sprites) # adds the sprite to the group
        for key, value in kwargs.items():
            setattr(self, key, value)
        # set additional custom properties
        for key, value in self.properties.items():
            setattr(self, key, value)
        
        self.size = (self.width, self.height)
        self.pos = (self.x, self.y)
        self.image = pg.Surface(self.size)
        self.image.fill(pg.Color('red'))
        self.rect = self.image.get_rect()
        self.rect.topleft = self.pos
            
    
    def update(self, dt):
        pass
    


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
        pass
    
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
        
        def startup(self):
            self.sprite.image = self.images[0].copy()
            self.sprite.rect = self.sprite.image.get_rect()
            self.sprite.rect.topleft = self.sprite.pos # only works when images are of the same size
            
            self.sprite.anim_timer = 0 # time in seconds
            self.sprite.anim_delay = 0.1 # animation delay in seconds
            self.sprite.anim_frame = 0 # current index of the images list
            
        
        def update(self, dt):
            self.sprite.animate(dt)
            keys = pg.key.get_pressed()
            if keys[pg.K_s]:
                self.done = True
            
    
    class Test_state(State):
        ''' for testing '''
        def __init__(self, sprite):
            super().__init__(sprite.game, sprite)
            self.next = 'Default_state'
        
        def startup(self):
            self.sprite.image = self.images[0].copy()
            self.sprite.rect = self.sprite.image.get_rect()
            self.sprite.rect.topleft = self.sprite.pos # only works when images are of the same size
            
            self.sprite.anim_timer = 0 # time in seconds
            self.sprite.anim_delay = 0.5 # animation delay in seconds
            self.sprite.anim_frame = 0 # current index of the images list
            
        
        def update(self, dt):
            self.sprite.animate(dt)
            
            keys = pg.key.get_pressed()
            if not keys[pg.K_s]:
                self.done = True
            
    
    
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







