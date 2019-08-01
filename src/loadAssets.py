import pygame as pg
import os


class Loader():
    def __init__(self, game):
        self.game = game
        base_dir = game.base_dir
        self.graphics_folder = os.path.join(base_dir, 'assets', 'graphics')
        self.sounds_folder = os.path.join(base_dir, 'assets', 'sounds')
        self.sprite_folder = os.path.join(self.graphics_folder, 'sprites')
        self.tileset_folder = os.path.join(self.graphics_folder, 'tilesets')
        
        
    def load_graphics(self):
        '''
        load sprite image strips here
        '''
        sprite_files = ['knight_strip.png']
        
        sprite_images = [pg.image.load(os.path.join(self.sprite_folder, f)).convert_alpha() 
                         for f in sprite_files]
                
        sprite_lib = {
                'knight_images': self.images_from_strip(sprite_images[0], 10)
                }
        
        return sprite_lib
        
    
    def images_from_strip(self, strip, number):
        img_w = strip.get_width() // number
        img_h = strip.get_height()
        
        images = []
        for i in range(number):
            s = strip.subsurface((i * img_w, 0, img_w, img_h))
            images.append(s)

        return images