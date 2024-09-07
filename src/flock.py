from typing import Set

import pygame as pg

from settings import FLOCK_COLOURS
from boid import Boid

class Flock:
    def __init__(self, _id: int):
        self.id = _id
        self.colour = FLOCK_COLOURS.get(_id, pg.Color("white"))
        self.boids: Set[Boid] = set()
    
    def add_boid(self, boid: Boid) -> None:
        self.boids.add(boid)
    
    def remove_boid(self, boid: Boid) -> None:
        self.boids.discard(boid)
    
    def update_and_draw(self, screen: pg.Surface, boids: Set[Boid], dt: float) -> None:
        for boid in self.boids:
            boid.update(boids, self.boids, dt)
            boid.draw(screen, self.colour)