from dataclasses import dataclass

@dataclass
class BoidConfig:
    min_speed: float
    max_speed: float
    size: float
    turn_speed: float
    vision_angle: float
    vision_distance: float
    protected_distance: float

DEFAULT_CONFIG = BoidConfig(
    min_speed=0.5,
    max_speed=1.0,
    size=10.0,
    turn_speed=0.015,
    vision_angle=270,
    vision_distance=120,
    protected_distance=60
)