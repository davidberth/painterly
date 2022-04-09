"""
This module contains the Context class, which is responsible for keeping track
of the current brush, transforms, and sample.
"""
import copy

from brush import Brush
from sampler import Sampler


class Context:
    brushes = []
    samplers = []
    opengl_ctx = None
    opengl_buffer = None
    shader = None
    fbo = None
    sample_number = 0
    last_coords = [(0, 0)]

    def set_brush(self, brush: Brush):
        if len(self.brushes) > 1:
            self.brushes[-1] = brush
        else:
            self.brushes.append(brush)

    @property
    def brush(self):
        return self.brushes[-1]

    def set_sampler(self, sampler: Sampler):
        if len(self.samplers) > 0:
            self.samplers[-1] = sampler
        else:
            self.samplers.append(sampler)

    @property
    def sampler(self):
        return self.samplers[-1]

    def set_last_coords(self, coords):
        if len(self.last_coords) > 0:
            self.last_coords[-1] = coords
        else:
            self.last_coords.append(coords)

    @property
    def last_coord(self):
        return self.last_coords[-1]

    def push(self):
        self.samplers.append(copy.deepcopy(self.sampler))
        self.brushes.append(copy.copy(self.brush))
        self.last_coords.append(copy.copy(self.last_coords))

    def pop(self):
        self.samplers.pop()
        self.brushes.pop()
        self.last_coords.pop()
