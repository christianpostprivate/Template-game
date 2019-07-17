import pygame as pg
from pytmx import TiledTileLayer, TiledObjectGroup
from pytmx.util_pygame import load_pygame
import inspect

from modules import sprites as spr

vec = pg.math.Vector2


class Map():
    def __init__(self, game, filename):
        self.game = game
        self.filename = filename
        
        # load map data
        self.tiled_map = load_pygame(self.filename)
        self.tilesize = vec(self.tiled_map.tilewidth, self.tiled_map.tileheight)
        self.size = vec(self.tiled_map.width * self.tilesize.x, 
                        self.tiled_map.height * self.tilesize.y)
        self.background_color = self.tiled_map.background_color
        
    
    def create_map(self):
        '''ectracts tileset and object data from a tmx file'''
        # create an empty surface 
        self.map_image = pg.Surface(self.size)
        # if background color was specified, fill the surface
        if self.background_color:
            self.map_image.fill(self.background_color)
        
        # loop through all available layers
        for layer in self.tiled_map:
            if isinstance(layer, TiledTileLayer):
                # if layer is tileset data, blit the tile image at the corresponding 
                # position on the map image
                for x, y, image in layer.tiles():
                    self.map_image.blit(image, (x * self.tilesize.x, 
                                                y * self.tilesize.y))
            elif isinstance(layer, TiledObjectGroup):
                # if layer is an object layer, fetch the corresponding sprite
                # from the sprites.py (spr) module
                sprites = dict(inspect.getmembers(spr, inspect.isclass))
                for obj in layer:
                    if obj.name in sprites:
                        # check if the sprite exists in sprites.py
                        # if so, instantiate the sprite
                        sprites[obj.name](self.game, **obj.__dict__)
                    else:
                        print(f'No sprite "{obj.name}" found in sprites module')


    def draw(self, screen, pos):
        screen.blit(self.map_image, pos)

