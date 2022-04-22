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
    left_margin = 0.0
    right_margin = 0.0
    offset = 0.0
    rotate = 0.0

    def __init__(self, coords=((0, 0), (0, 0)), num_samples=1, margin=None,
                 left_margin=None, right_margin=None, rotate=0.0):
        self.num_samples = int(num_samples + 0.5)
        num_coords = len(coords)

        if margin:
            self.left_margin = margin
            self.right_margin = margin
        if left_margin:
            self.left_margin = left_margin
        if right_margin:
            self.right_margin = right_margin
        self.x_coords = []
        self.y_coords = []
        self.angles = []
        self.rotate = rotate
        for t in np.linspace(self.left_margin, 1.0 - self.right_margin,
                             self.num_samples):
            left_index = int(t * (num_coords - 1) - 0.01)
            right_index = left_index + 1
            inner_t = t * (num_coords - 1) - left_index
            ix1, iy1 = coords[left_index]
            ix2, iy2 = coords[right_index]
            angle = np.arctan2(iy2 - iy1, ix2 - ix1)
            self.x_coords.append(ix1 * (1 - inner_t) + ix2 * inner_t)
            self.y_coords.append(iy1 * (1 - inner_t) + iy2 * inner_t)
            self.angles.append(angle)

    def get_coord(self, coord_number: int):
        return self.x_coords[coord_number], self.y_coords[coord_number]

    def get_angle(self, coord_number: int):
        return self.angles[coord_number]

    def transform(self, x, y, coord_number):
        bx, by = self.get_coord(coord_number)
        angle = self.get_angle(coord_number) * self.rotate
        cos_angle = np.cos(angle)
        sin_angle = np.sin(angle)

        nx = bx + x * cos_angle - y * sin_angle
        ny = by + x * sin_angle + y * cos_angle
        return nx, ny

    def __repr__(self):
        return str(self.x_coords) + ' - ' + str(self.y_coords)
