import pygame as pg
import traceback

from modules import game



if __name__ == '__main__':
    try:
        g = game.Game()
        g.run()
    except:
        traceback.print_exc()
        pg.quit()