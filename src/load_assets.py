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
        sprite_files = list(filter(lambda x: x[-3:]=='png', os.listdir(self.sprite_folder)))
        sprite_images = [pg.image.load(os.path.join(self.sprite_folder, f)).convert_alpha() 
                         for f in sprite_files]
        
        # create a dictionary with name: list of images
        sprite_lib = {
            'example': self.images_from_strip(sprite_images['example'], 16)
            }
        
        return sprite_lib
    
    
    def load_sounds(self):
        pg.mixer.init()
        
        bgm_folder = os.path.join(self.sounds_folder, 'bgm')
        sfx_folder = os.path.join(self.sounds_folder, 'sfx')
        
        music_files = list(filter(lambda x: x[-3:]=='mp3' or x[-3:]=='ogg', 
                                  os.listdir(bgm_folder)))
        music_objects = {f[:-4]: os.path.join(bgm_folder, f)
                         for f in music_files}
        
        sfx_files = list(filter(lambda x: x[-3:]=='mp3' or x[-3:]=='wav', 
                                  os.listdir(sfx_folder)))
        sfx_objects = {f[:-4]: pg.mixer.Sound(os.path.join(sfx_folder, f))
                        for f in sfx_files}
        
        # sound libs stored as (filename, relative volume)
        self.music_lib = {
                }
        
        self.sfx_lib = {
            'Pickup_Coin35': (sfx_objects['Pickup_Coin35.wav'], 1),
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