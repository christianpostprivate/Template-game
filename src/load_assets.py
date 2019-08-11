import pygame as pg
import os

import settings as st


# TODO: multiple music channels?

class Loader():
    def __init__(self, game):
        self.game = game
        base_dir = game.base_dir
        self.graphics_folder = os.path.join(base_dir, 'assets', 'graphics')
        self.sounds_folder = os.path.join(base_dir, 'assets', 'sounds')
        self.sprite_folder = os.path.join(self.graphics_folder, 'sprites')
        self.tileset_folder = os.path.join(self.graphics_folder, 'tilesets')
        
        self.channel = None
        
        
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
    
    
    def load_sounds(self):
        pg.mixer.init()
        
        music_files = [
                'A_Journey_Awaits.mp3'
                ]
        sfx_files = [
                'Pickup_Coin35.wav'
                ]

        music_objects = [os.path.join(self.sounds_folder, 'bgm', f)
                         for f in music_files]     
        sfx_objects = [pg.mixer.Sound(os.path.join(self.sounds_folder, 'sfx', f))
                        for f in sfx_files]
        
        # sound libs stored as (filename, relative volume)
        self.music_lib = {
                'overworld': (music_objects[0], 0.9)
                }
        
        self.sfx_lib = {
                'test_sound': (sfx_objects[0], 1)
                }
        
        
    def play_music(self, key, loop=True):
        if loop:
            loops = -1
        else:
            loops = 0
        pg.mixer.music.load(self.music_lib[key][0])
        pg.mixer.music.play(loops)
        volume = st.MUSIC_VOLUME * self.music_lib[key][1]
        pg.mixer.music.set_volume(volume)
        
          
    def play_sound(self, key):
        sound = self.sfx_lib[key][0]
        volume = st.SFX_VOLUME * self.sfx_lib[key][1]
        sound.set_volume(volume)
        # play the sound if it isn't already being played
        if self.channel is None:
            self.channel = sound.play()
        else:
            if self.channel.get_sound() == sound:
                if not self.channel.get_busy():
                    self.channel = sound.play()
            else:
                self.channel = sound.play()
            
    
    def images_from_strip(self, strip, number):
        img_w = strip.get_width() // number
        img_h = strip.get_height()
        
        images = []
        for i in range(number):
            s = strip.subsurface((i * img_w, 0, img_w, img_h))
            images.append(s)

        return images