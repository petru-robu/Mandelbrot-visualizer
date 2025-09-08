# viewport.py
from dataclasses import dataclass

@dataclass
class Viewport:
    vp_width: int
    vp_height: int
    world_width: float
    center: complex

    @property
    def scale(self) -> float:
        return self.world_width / self.vp_width

    @property
    def world_height(self) -> float:
        return self.scale * self.vp_height
    
    @property
    def offset(self) -> complex:
        return (self.center + complex(-self.world_width, self.world_height) / 2)

    def translate_position(self, pos_x:int, pos_y:int) -> complex:
        return (complex(pos_x, -pos_y) * self.scale + self.offset)
