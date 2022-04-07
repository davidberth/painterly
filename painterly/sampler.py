"""
This module contains the Brush class, which is responsible for keeping track
of the current properties of a brush such as the thickness, scattering, color, and alpha.
"""
from dataclasses import dataclass
from enum import Enum, auto


class SamplerType(Enum):
    EQUAL = auto()
    RANDOM = auto()


@dataclass
class Sampler:
    # By default, we have a simple equal sampler with one sample
    sampler_type = SamplerType.EQUAL
    num_samples = 1
