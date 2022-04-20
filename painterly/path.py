"""
This module contains the Path class, which is responsible for keeping track
of individual brush stroke segments.
"""
from dataclasses import dataclass

import numpy as np


@dataclass
class Path:
    x1: float = 0.0
    y1: float = 0.0
    x2: float = 0.0
    y2: float = 0.0
    curve: float = 0.0
    wavy: float = 0.0

    def get_path_vertices(self):
        x1 = self.x1
        y1 = self.y1
        x2 = self.x2
        y2 = self.y2

        curve = self.curve
        wavy = self.wavy

        path_vertices = []

        normalized_direction = np.array((x2 - x1, y2 - y1),
                                        dtype=np.float32)
        stroke_distance = np.sqrt(
            normalized_direction[0] ** 2 + normalized_direction[1] ** 2)
        normalized_direction /= stroke_distance
        orthogonal_direction = np.array(
            (-normalized_direction[1], normalized_direction[0]))

        for t in np.arange(0.0, 1.002, 0.04):
            x = x1 * (1.0 - t) + x2 * t
            y = y1 * (1.0 - t) + y2 * t
            path_curve = np.sqrt(
                1 - (t * 2.0 - 1) ** 2) * curve * stroke_distance * 0.5
            path_wave = np.sin(t * 4.0) * wavy * np.random.uniform(0.8, 1.2)
            px1 = x + orthogonal_direction[0] * (path_curve + path_wave)
            py1 = y + orthogonal_direction[1] * (path_curve + path_wave)

            path_vertices.append((px1, py1))

        return path_vertices