"""
This module contains the Context class, which is responsible for keeping track
of the current brush, transforms, and sample.
"""
from dataclasses import dataclass


@dataclass
class Context:
    brush: Brush
    transform: Transform
    sample: Sample


