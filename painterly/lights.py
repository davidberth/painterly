"""
This module keeps track of the set of lights for each layer.
"""
from light import Light


class Lights:
    lights = []

    def add_light(self, x, y, hue, sat, bright, alpha, radius):
        self.lights.append(Light(x, y, hue, sat, bright, alpha, radius))

    def render(self, ctx):
        for light in self.lights:
            light.render(ctx)
