"""
This module contains the Context class, which is responsible for keeping track
of the current brush, transforms, and sample.
"""
from dataclasses import dataclass

from brush import Brush
from sampler import Sampler


@dataclass
class Context:
    brush: Brush = Brush()
    sampler: Sampler = Sampler()
    opengl_ctx = None
    opengl_buffer = None
    shader = None
    fbo = None
