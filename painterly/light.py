"""
This module implements point lights.
"""
from dataclasses import dataclass

import numpy as np


@dataclass
class Light:
    x: float = 0.0
    y: float = 0.0
    red: float = 0.0
    green: float = 0.0
    blue: float = 0.0
    intensity: float = 0.0

    def compute_impact(self, tx, ty):
        dis = np.sqrt((tx - self.x) ** 2 + (ty - self.y) ** 2)
        dis /= self.intensity
        impact = max(1.0 - dis, 0.0) / 2.0
        return impact
