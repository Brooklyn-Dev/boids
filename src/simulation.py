from random import choice, randrange, uniform

import pygame as pg

from settings import BOID_SIZE, FPS, SCREEN_WIDTH, SCREEN_HEIGHT, MAX_SPEED, MIN_SPEED, NUM_BOIDS
from boid import Boid

class Simulation:
    def __init__(self) -> None:
        pg.init()
        
        self.screen: pg.Surface = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pg.display.set_caption("Boids")
        self.clock: pg.Clock = pg.time.Clock()
        
        self.boids = []
        for _ in range(NUM_BOIDS):
            pos: pg.Vector2 = pg.Vector2(randrange(0, SCREEN_WIDTH), randrange(0, SCREEN_HEIGHT))
            vel: pg.Vector2 = pg.Vector2(uniform(MIN_SPEED, MAX_SPEED) * choice((-1, 1)), uniform(MIN_SPEED, MAX_SPEED) * choice((-1, 1)))
            self.boids.append(Boid(BOID_SIZE, pos, vel))
        
        self.running: bool = True
        
    def _handle_input(self) -> None:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
        
    def run(self) -> None:
        while self.running:
            self._handle_input()
            
            self.screen.fill(pg.Color('black'))
            
            for boid in self.boids:
                boid.update()
                boid.draw(self.screen)
            
            pg.display.flip()
            self.clock.tick(FPS)
        
        pg.quit()
