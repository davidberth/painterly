"""
This module keeps track of the set of lights for each layer.
"""
from light import Light


class Lights:
    lights = []

    def add_light(self, x, y, intensity):
        self.lights.append(Light(x, y, 1.0, 1.0, 1.0, intensity))
