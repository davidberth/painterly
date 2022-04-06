"""
This module contains the Brush class, which is responsible for keeping track
of the current properties of a brush such as the thickness, scattering, color, and alpha.
"""
from dataclasses import dataclass


@dataclass
class Brush:
    # by default, we have a simple black brush used for the outlines of objects
    # in Chinese style paintings
    thick: float = 0.001
    hue: float = 0.0
    sat: float = 0.0
    value: float = 0.0
    alpha: float = 0.9
