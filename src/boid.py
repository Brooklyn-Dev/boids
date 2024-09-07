from math import atan2, degrees 
from typing import Tuple

import pygame as pg

from settings import MAX_SPEED, MIN_SPEED, SCREEN_MARGIN_LEFT, SCREEN_MARGIN_RIGHT, SCREEN_MARGIN_TOP, SCREEN_MARGIN_BOTTOM, TURN_SPEED

class Boid:
    def __init__(self, size: float, position: pg.Vector2, velocity: pg.Vector2) -> None:
        self.size: float = abs(size)
        
        self.position: pg.Vector2 = position
        self.velocity: pg.Vector2 = velocity.clamp_magnitude(MIN_SPEED, MAX_SPEED)

    def update(self) -> None:
        self._avoid_screen_edges()
        
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
        
    def _avoid_screen_edges(self) -> None:
        if self.position.x < SCREEN_MARGIN_LEFT:
            self.apply_force(pg.Vector2(TURN_SPEED, 0))
        if self.position.x > SCREEN_MARGIN_RIGHT:
            self.apply_force(pg.Vector2(-TURN_SPEED, 0))
        if self.position.y < SCREEN_MARGIN_TOP:
            self.apply_force(pg.Vector2(0, TURN_SPEED))
        if self.position.y > SCREEN_MARGIN_BOTTOM:
            self.apply_force(pg.Vector2(0, -TURN_SPEED))