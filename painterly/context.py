"""
This module contains the Context class, which is responsible for keeping track
of the current brush, transforms, and sample.
"""

from sampler import Sampler


class Context:
    brushes = []
    samplers = []
    opengl_ctx = None
    opengl_buffer = None
    shader = None
    fbo = None

    def add_brush(self, brush):
        self.brushes.append(brush)

    def replace_brush(self, brush):
        if len(self.brushes) > 1:
            self.brushes[-1] = brush

    def pop_push(self):
        self.brushes.pop()

    @property
    def brush(self):
        if len(self.brushes) < 1:
            return None
        return self.brushes[-1]

    def add_sampler(self, sampler: Sampler):
        self.samplers.append(sampler)

    def replace_sampler(self, sampler: Sampler):
        self.samplers[-1] = sampler

    def pop_sampler(self):
        self.samplers.pop()

    @property
    def sampler(self):
        if len(self.samplers) < 1:
            return None
        return self.samplers[-1]
