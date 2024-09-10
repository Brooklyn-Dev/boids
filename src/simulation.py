from random import choice, randrange, uniform
import time
from typing import List, Set, Tuple

import pygame as pg

from settings import FPS, SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_MARGIN_LEFT, SCREEN_MARGIN_RIGHT, SCREEN_MARGIN_TOP, SCREEN_MARGIN_BOTTOM, NUM_BOIDS, NUM_FLOCKS
from boid_config import DEFAULT_CONFIG
from boid import Boid
from flock import Flock

class Simulation:
    def __init__(self) -> None:
        pg.init()
        
        self.screen: pg.Surface = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pg.display.set_caption("Boids")
        self.clock: pg.Clock = pg.time.Clock()
        
        self._generate_flocks_and_boids()
        self.selected_boid: Boid | None = None

        self.running: bool = True
        
    def _generate_flocks_and_boids(self) -> None:
        self.flocks: List[Flock] = [Flock(_id=i) for i in range(NUM_FLOCKS)]
        self.boids: Set[Boid] = set()
        
        for i in range(NUM_BOIDS):
            pos: pg.Vector2 = pg.Vector2(randrange(SCREEN_MARGIN_LEFT, SCREEN_MARGIN_RIGHT), randrange(SCREEN_MARGIN_TOP, SCREEN_MARGIN_BOTTOM))
            vel: pg.Vector2 = pg.Vector2(
                uniform(DEFAULT_CONFIG.min_speed, DEFAULT_CONFIG.max_speed) * choice((-1, 1)),
                uniform(DEFAULT_CONFIG.min_speed, DEFAULT_CONFIG.max_speed) * choice((-1, 1))
            )
            
            boid: Boid = Boid(pos, vel, config=DEFAULT_CONFIG, flock_id=(i % NUM_FLOCKS))
            self.boids.add(boid)
            self.flocks[i % NUM_FLOCKS].add_boid(boid)
 
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
        dt: float = 0
        prev_time: float = time.time()
        
        while self.running:
            self._handle_input()
            
            self.screen.fill(pg.Color('black'))
            
            for flock in self.flocks:
                flock.update_and_draw(self.screen, self.boids, dt)
            
            pg.display.flip()
            
            dt = time.time() - prev_time
            prev_time = time.time()
            
            self.clock.tick(FPS)
        
        pg.quit()