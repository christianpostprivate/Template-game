import pygame as pg


# TODO: make seperate parent classes for Sprite and animated sprite



class Test_sprite(pg.sprite.Sprite):
    ''' basic sprite class for testing'''
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