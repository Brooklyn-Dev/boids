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
    min_speed=0.5,
    max_speed=1.0,
    size=10.0,
    separate_speed=0.002,
    align_speed=0.002,
    centre_speed=0.002,
    turn_speed=0.05,
    vision_angle=270,
    vision_distance=120,
    protected_distance=30
)