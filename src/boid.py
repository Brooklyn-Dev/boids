from math import atan2, cos, degrees, radians, sin
from typing import Tuple

import pygame as pg

from settings import SCREEN_MARGIN_LEFT, SCREEN_MARGIN_RIGHT, SCREEN_MARGIN_TOP, SCREEN_MARGIN_BOTTOM
from boid_config import BoidConfig, DEFAULT_CONFIG

class Boid:
    def __init__(self, position: pg.Vector2, velocity: pg.Vector2, config: BoidConfig = DEFAULT_CONFIG) -> None:
        self._config = config
        self.size: float = config.size
        
        self._position: pg.Vector2 = position
        self._velocity: pg.Vector2 = velocity.clamp_magnitude(config.min_speed, config.max_speed)
        self.selected: bool = False

    @property
    def position(self) -> pg.Vector2:
        return self._position

    @property
    def velocity(self) -> pg.Vector2:
        return self._velocity
    
    def get_bounding_box(self) -> pg.Rect:
        return pg.Rect(
            self._position.x - self.size,
            self._position.y - self.size,
            self.size * 2,
            self.size * 2
        )

    def update(self) -> None:
        self._avoid_screen_edges()
        # self._avoid_local_flockmates()
        
        self._velocity.clamp_magnitude_ip(self._config.min_speed, self._config.max_speed)
        self._position += self._velocity
        
    def draw(self, screen: pg.Surface) -> None:
        orientation_angle: float = degrees(atan2(self._velocity.y, self._velocity.x))
        
        if self.selected:
            self._draw_vision_disc(screen, orientation_angle)
        
        point1: pg.Vector2 = self._position + pg.Vector2(self.size, 0).rotate(orientation_angle)
        point2: pg.Vector2 = self._position + pg.Vector2(-self.size * 0.5, self.size * 0.5).rotate(orientation_angle)
        point3: pg.Vector2 = self._position + pg.Vector2(-self.size * 0.5, -self.size * 0.5).rotate(orientation_angle)

        points: Tuple[pg.Vector2] = (point1, point2, point3)
        
        pg.draw.polygon(screen, pg.Color("white"), points)
        
        if self.selected:
            bounding_box = self.get_bounding_box()
            pg.draw.rect(screen, pg.Color("red"), bounding_box, 2)

    def _draw_vision_disc(self, screen: pg.Surface, orientation_angle: float) -> None:
        r = self._config.vision_distance
        
        disc_surface = pg.Surface((r * 2, r * 2), pg.SRCALPHA)
        
        start_angle = radians(-self._config.vision_angle / 2)
        end_angle = radians(self._config.vision_angle / 2)
        
        center = (r, r)
        points = [center]
        num_segments = 64
        
        # Calculate points across the arc of a circular sector
        for i in range(num_segments + 1):
            Θ = start_angle + (end_angle - start_angle) * i / num_segments
            
            # Polar to Cartesian Coordinates: x = r cosΘ, y = r sinΘ
            # https://en.wikipedia.org/wiki/Polar_coordinate_system#Converting_between_polar_and_Cartesian_coordinates
            
            x = r + r * cos(Θ)
            y = r + r * sin(Θ)
            
            points.append((x, y))
        
        points.append(center)
        
        pg.draw.polygon(disc_surface, pg.Color(128, 128, 128, 64), points)
        
        rotated_disc_surf = pg.transform.rotate(disc_surface, -orientation_angle)
        rotated_rect = rotated_disc_surf.get_rect(center=self._position)
        
        screen.blit(rotated_disc_surf, rotated_rect.topleft)

    def apply_force(self, force: pg.Vector2) -> None:
        self._velocity += force
        
    def _avoid_screen_edges(self) -> None:
        if self._position.x < SCREEN_MARGIN_LEFT:
            self.apply_force(pg.Vector2(self._config.turn_speed, 0))
            
        if self._position.x > SCREEN_MARGIN_RIGHT:
            self.apply_force(pg.Vector2(-self._config.turn_speed, 0))
            
        if self._position.y < SCREEN_MARGIN_TOP:
            self.apply_force(pg.Vector2(0, self._config.turn_speed))
            
        if self._position.y > SCREEN_MARGIN_BOTTOM:
            self.apply_force(pg.Vector2(0, -self._config.turn_speed))
            
    # Separation
    def _avoid_local_flockmates(self) -> None:
        raise NotImplementedError()