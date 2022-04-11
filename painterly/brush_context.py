"""
This module contains the BrushContext class, which is responsible for keeping track
of the current brush, path, transforms, and samplers.
"""

from brush import Brush
from sampler import Sampler


class BrushContext:
    def __init__(self):
        self.brush = Brush()
        self.sampler = Sampler()
        self.sample_number = 0
        self.path_coords = (0, 0)

    def set_path_coords(self, path):
        self.path_coords = path