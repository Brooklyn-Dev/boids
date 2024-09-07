from random import choice, randrange, uniform
from typing import List, Tuple

import pygame as pg

from settings import FPS, SCREEN_WIDTH, SCREEN_HEIGHT, NUM_BOIDS
from boid_config import DEFAULT_CONFIG
from boid import Boid

class Simulation:
    def __init__(self) -> None:
        pg.init()
        
        self.screen: pg.Surface = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pg.display.set_caption("Boids")
        self.clock: pg.Clock = pg.time.Clock()
        
        self.selected_boid: Boid | None = None
        
        self.boids: List[Boid] = []
        for _ in range(NUM_BOIDS):
            pos: pg.Vector2 = pg.Vector2(randrange(0, SCREEN_WIDTH), randrange(0, SCREEN_HEIGHT))
            vel: pg.Vector2 = pg.Vector2(
                uniform(DEFAULT_CONFIG.min_speed, DEFAULT_CONFIG.max_speed) * choice((-1, 1)),
                uniform(DEFAULT_CONFIG.min_speed, DEFAULT_CONFIG.max_speed) * choice((-1, 1))
            )
            self.boids.append(Boid(pos, vel, DEFAULT_CONFIG))
        
        self.running: bool = True
        
    def _handle_input(self) -> None:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
                
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1: # Left click
                    mouse_pos: Tuple[int, int] = pg.mouse.get_pos()
                    for boid in self.boids:
                        if boid.get_bounding_box().collidepoint(mouse_pos):
                            if self.selected_boid is not None:
                                self.selected_boid.selected = False
                                
                            if boid != self.selected_boid:
                                boid.selected = True
                                self.selected_boid = boid
                            else:
                                self.selected_boid = None
                                
                            break
        
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
