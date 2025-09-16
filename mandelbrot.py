# mandelbrot.py
from dataclasses import dataclass
from math import log
import numpy as np
from numba import njit, prange

@njit(fastmath=True)
def escape_count_numba(c_real: float, c_imag: float, max_iter: int, escape_radius_sq: float, smooth: bool) -> float:
    z_real, z_imag = 0.0, 0.0
    for i in range(max_iter):
        temp = z_real * z_real - z_imag * z_imag + c_real
        z_imag = 2.0 * z_real * z_imag + c_imag
        z_real = temp

        if z_real * z_real + z_imag * z_imag > escape_radius_sq:
            if smooth:
                modulus = (z_real * z_real + z_imag * z_imag) ** 0.5
                return i + 1 - log(log(modulus)) / log(2)
            return i
    return max_iter

@dataclass
class MandelbrotSet:
    max_iterations: int
    escape_radius: float = 2.0

    def escape_count(self, c: complex, smooth=False) -> float:
        return escape_count_numba(
            c.real, c.imag,
            self.max_iterations,
            self.escape_radius * self.escape_radius,
            smooth
        )

    def stability(self, c: complex, smooth=False, clamp=True) -> float:
        val = self.escape_count(c, smooth) / self.max_iterations
        return max(0.0, min(val, 1.0)) if clamp else val
