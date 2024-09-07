from dataclasses import dataclass

@dataclass
class BoidConfig:
    min_speed: float
    max_speed: float
    size: float
    separate_speed: float
    align_speed: float
    centre_speed: float
    turn_speed: float
    vision_angle: float
    vision_distance: float
    protected_distance: float

DEFAULT_CONFIG = BoidConfig(
    min_speed=50,
    max_speed=120,
    size=10,
    separate_speed=80,
    align_speed=10,
    centre_speed=40,
    turn_speed=1200,
    vision_angle=270,
    vision_distance=80,
    protected_distance=20
)