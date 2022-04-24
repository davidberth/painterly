"""
This module contains the BrushContext class, which is responsible for keeping track
of the current brush, path, transforms, and samplers.
"""
from dataclasses import dataclass

from brush import Brush
from sampler import Sampler


@dataclass
class BrushContext:
    brush = Brush()
    sampler = Sampler()
    path_coords = [(0.499, 0.5), (0.501, 0.5)]

    def set_path_coords(self, path):
        self.path_coords = path
