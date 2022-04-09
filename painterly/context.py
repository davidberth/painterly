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

    # TODO remove duplication - same behavior with brush and sampler
    def push_brush(self):
        self.brushes.append(self.brushes[-1])

    def add_brush(self, brush: Brush):
        self.brushes.append(brush)

    def replace_brush(self, brush):
        if len(self.brushes) > 1:
            self.brushes[-1] = copy.deepcopy(brush)

    def pop_brush(self):
        self.brushes.pop()

    @property
    def brush(self):
        if len(self.brushes) < 1:
            return None
        return self.brushes[-1]

    def push_sampler(self):
        if len(self.samplers) > 0:
            self.samplers.append(copy.deepcopy(self.samplers[-1]))
        else:
            self.samplers.append(Sampler([[0.0, 0.0], [0.0, 0.0]], 1))

    def add_sampler(self, sampler: Sampler):
        self.samplers.append(sampler)

    def replace_sampler(self, sampler: Sampler):
        if len(self.samplers) > 0:
            self.samplers[-1] = sampler
        else:
            self.samplers.append(sampler)

    def pop_sampler(self):
        self.samplers.pop()

    @property
    def sampler(self):
        if len(self.samplers) < 1:
            return None
        return self.samplers[-1]
