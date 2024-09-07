from math import atan2, degrees 
from typing import Tuple

import pygame as pg

from settings import MAX_SPEED, MIN_SPEED

class Boid:
    def __init__(self, size: float, position: pg.Vector2, velocity: pg.Vector2) -> None:
        self.size = abs(size)
        
        self.position: pg.Vector2 = position
        self.velocity: pg.Vector2 = velocity

    def update(self) -> None:
        self.position += self.velocity
        
    def draw(self, screen: pg.Surface) -> None:
        angle: float = degrees(atan2(self.velocity.y, self.velocity.x))
        
        point1: pg.Vector2 = self.position + pg.Vector2(self.size, 0).rotate(angle)
        point2: pg.Vector2 = self.position + pg.Vector2(-self.size * 0.5, self.size * 0.5).rotate(angle)
        point3: pg.Vector2 = self.position + pg.Vector2(-self.size * 0.5, -self.size * 0.5).rotate(angle)

        points: Tuple[pg.Vector2] = (point1, point2, point3)
        
        pg.draw.polygon(screen, pg.Color("white"), points)

    def apply_force(self, force: pg.Vector2) -> None:
        self.velocity += force
        self.velocity.clamp_magnitude_ip(MIN_SPEED, MAX_SPEED)