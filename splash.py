import pygame as pg

import tools, prepare
from state_engine import GameState



class Splash(GameState):
    def __init__(self):
        super(Splash, self).__init__()
          
    def startup(self, persistent):
        self.persist = persistent
        
    def get_event(self, event):
        if event.type == pg.QUIT:
            self.quit = True
        elif event.type == pg.KEYUP:
            if event.key == pg.K_ESCAPE:
                self.quit = True
        elif event.type == pg.MOUSEBUTTONUP:
            self.done = True
            self.next_state = "GAMEPLAY"
                
    def update(self, dt):
        pass
        
    def draw(self, surface):
        surface.fill(pg.Color("dodgerblue"))