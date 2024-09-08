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
    max_speed=100,
    size=10,
    separate_speed=800,
    align_speed=1,
    centre_speed=0.2,
    turn_speed=300,
    vision_angle=270,
    vision_distance=90,
    protected_distance=30
)