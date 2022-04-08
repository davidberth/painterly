"""
This module contains the Brush class, which is responsible for keeping track
of the current properties of a brush such as the thickness, scattering, color, and alpha.
"""
from enum import Enum, auto

import numpy as np


class SamplerType(Enum):
    EQUAL = auto()
    RANDOM = auto()


class Sampler:

    def __init__(self, coords, num_samples):
        self.num_samples = int(num_samples + 0.5)
        x, y = coords
        x1, y1 = x[0], y[0]
        x2, y2 = x[-1], y[-1]
        self.x_coords = []
        self.y_coords = []
        for t in np.linspace(0.0, 1.0, self.num_samples):
            self.x_coords.append(x1 * (1 - t) + x2 * t)
            self.y_coords.append(y1 * (1 - t) + y2 * t)

    def get_coord(self, coord_number: int):
        return self.x_coords[coord_number], self.y_coords[coord_number]
