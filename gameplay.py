import pygame as pg

import tools, prepare
from state_engine import GameState
from grid import Grid


class Gameplay(GameState):
    def __init__(self):
        super(Gameplay, self).__init__()
        self.grid = Grid()
        self.sim_speed = 45
        self.timer = 0
        
    def startup(self, persistent):
        self.persist = persistent

    def get_event(self,event):
        if event.type == pg.QUIT:
            self.quit = True
        elif event.type == pg.KEYUP:
            if event.key == pg.K_ESCAPE:
                self.quit = True
            
    def update(self, dt):
        self.timer += dt
        while self.timer > self.sim_speed:
            self.grid.update(self.sim_speed)
            self.timer -= self.sim_speed

    def draw(self, surface):
        self.grid.draw(surface)
        