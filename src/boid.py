from math import atan2, cos, degrees, radians, sin
from typing import List, Set, Tuple

import pygame as pg

from settings import SCREEN_MARGIN_LEFT, SCREEN_MARGIN_RIGHT, SCREEN_MARGIN_TOP, SCREEN_MARGIN_BOTTOM
from boid_config import BoidConfig, DEFAULT_CONFIG

class Boid:
    @property
    def position(self) -> pg.Vector2:
        return self._position

    @property
    def velocity(self) -> pg.Vector2:
        return self._velocity    
    
    def __init__(self, position: pg.Vector2, velocity: pg.Vector2, config: BoidConfig = DEFAULT_CONFIG, flock_id: int = 0) -> None:
        self._config: BoidConfig = config
        self.colour: pg.Color = pg.Color("white")
        self.size: float = config.size
        self.vision_distance_squared: float = self._config.vision_distance ** 2
        self.protected_distance_squared: float = self._config.protected_distance ** 2
        self.half_vision_angle: float = self._config.vision_angle / 2
        
        self._position: pg.Vector2 = position
        self._velocity: pg.Vector2 = velocity.clamp_magnitude(config.min_speed, config.max_speed)
        self.selected: bool = False

    def get_bounding_box(self) -> pg.Rect:
        return pg.Rect(
            self._position.x - self.size,
            self._position.y - self.size,
            self.size * 2,
            self.size * 2
        )

    def update(self, boids: Set["Boid"], flockmates: Set["Boid"], dt: float) -> None:
        self._avoid_screen_edges(dt)
        self._avoid_all_boids(boids, dt)
        # self._align_with_flockmates(flockmates, dt)
        
        self._velocity.clamp_magnitude_ip(self._config.min_speed, self._config.max_speed)
        self._position += self._velocity * dt
        
    def draw(self, screen: pg.Surface, colour: pg.Color = pg.Color("White")) -> None:
        orientation_angle: float = degrees(atan2(self._velocity.y, self._velocity.x))
        
        if self.selected:
            self._draw_discs(screen, orientation_angle)
        
        point1: pg.Vector2 = self._position + pg.Vector2(self.size, 0).rotate(orientation_angle)
        point2: pg.Vector2 = self._position + pg.Vector2(-self.size * 0.5, self.size * 0.5).rotate(orientation_angle)
        point3: pg.Vector2 = self._position + pg.Vector2(-self.size * 0.5, -self.size * 0.5).rotate(orientation_angle)

        points: Tuple[pg.Vector2] = (point1, point2, point3)
        
        pg.draw.polygon(screen, colour, points)
        
        if self.selected:
            bounding_box = self.get_bounding_box()
            pg.draw.rect(screen, pg.Color("red"), bounding_box, width=2)

    # Draw vision disc and protected disc
    def _draw_discs(self, screen: pg.Surface, orientation_angle: float) -> None:
        radius: float = self._config.vision_distance
        
        disc_surface: pg.Surface = pg.Surface((radius * 2, radius * 2), pg.SRCALPHA)
        
        start_angle: float = radians(-self._config.vision_angle / 2)
        end_angle: float = radians(self._config.vision_angle / 2)
        centre: pg.Vector2 = pg.Vector2(radius, radius)
        
        points: List[pg.Vector2] = self._calc_disc_points(start_angle, end_angle, 64, radius, centre)
        pg.draw.polygon(disc_surface, pg.Color(128, 128, 128, 64), points)
        
        points = self._calc_disc_points(start_angle, end_angle, 64, self._config.protected_distance, centre)
        pg.draw.polygon(disc_surface, pg.Color(128, 128, 128, 128), points)
        
        rotated_disc_surf = pg.transform.rotate(disc_surface, -orientation_angle)
        rotated_rect = rotated_disc_surf.get_rect(center=self._position)
        
        screen.blit(rotated_disc_surf, rotated_rect.topleft)
        
    # Calculate points across the arc of a circular sector and then the centre to form a disc
    def _calc_disc_points(self, start_angle: float, end_angle: float, num_segments: int, radius: float, centre: pg.Vector2) -> List[pg.Vector2]:
        points: List[pg.Vector2] = [centre]
        
        for i in range(num_segments + 1):
            Θ: float = start_angle + (end_angle - start_angle) * i / num_segments
            
            # Polar to Cartesian Coordinates: x = r cosΘ, y = r sinΘ
            # https://en.wikipedia.org/wiki/Polar_coordinate_system#Converting_between_polar_and_Cartesian_coordinates
            x: float = centre.x + radius * cos(Θ)
            y: float = centre.y + radius * sin(Θ)
            
            points.append(pg.Vector2(x, y))
            
        points.append(centre)
        
        return points

    def apply_force(self, force: pg.Vector2, dt: float) -> None:
        self._velocity += force * dt
        
    def _avoid_screen_edges(self, dt: float) -> None:
        if self._position.x < SCREEN_MARGIN_LEFT:
            self.apply_force(pg.Vector2(self._config.turn_speed, 0), dt)
            
        if self._position.x > SCREEN_MARGIN_RIGHT:
            self.apply_force(pg.Vector2(-self._config.turn_speed, 0), dt)
            
        if self._position.y < SCREEN_MARGIN_TOP:
            self.apply_force(pg.Vector2(0, self._config.turn_speed), dt)
            
        if self._position.y > SCREEN_MARGIN_BOTTOM:
            self.apply_force(pg.Vector2(0, -self._config.turn_speed), dt)
            
    # Separation
    def _avoid_all_boids(self, boids: Set["Boid"], dt: float) -> None:
        for boid in boids:
            if boid is self:
                continue
                
            dist: pg.Vector2 = self.position - boid.position
            
            if dist.length_squared() >= self.protected_distance_squared:
                continue
            
            angle_to_boid: float = self.position.angle_to(dist) # 0 = right
            
            if -self.half_vision_angle <= angle_to_boid <= self.half_vision_angle:
                self.apply_force(dist * self._config.separate_speed, dt)
            
    # Alignment
    def _align_with_flockmates(self, flockmates: Set["Boid"], dt: float) -> None:
        raise NotImplementedError("the method '_align_with_flockmates' is not yet implemented")
        
        # for mate in flockmates:
        #     if mate is self:
        #         continue