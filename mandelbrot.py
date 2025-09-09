# mandelbrot.py
from dataclasses import dataclass
from math import log

@dataclass
class MandelbrotSet:
    max_iterations: int
    escape_radius: float = 2.0

    def escape_count(self, c: complex, smooth=False) -> int | float:
        z = 0
        for i in range(self.max_iterations):
            z = z * z + c
            if abs(z) > self.escape_radius:
                if smooth:
                    return i + 1 - log(log(abs(z))) / log(2)
        return self.max_iterations
    
    def stability(self, c: complex, smooth=False, clamp=True) -> float:
        val = self.escape_count(c, smooth) / self.max_iterations
        return max(0.0, min(val, 1.0)) if clamp else val

    def __contains__(self, c:complex) -> bool:
        return self.stability(c) == 1        
    


