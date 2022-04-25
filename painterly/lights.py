"""
This module keeps track of the set of lights for each layer.
"""

from light import Light

MAX_LIGHTS = 100


class Lights:
    lights = []

    def add_light(self, x, y, hue, sat, bright, alpha, radius):
        self.lights.append(Light(x, y, hue, sat, bright, alpha, radius))

    def set_uniform(self, opengl_ctx):
        shader = opengl_ctx.brush_shader
        num_lights = len(self.lights)
        shader['num_lights'].value = num_lights
        # set the light positions
        light_positions = shader['light_positions']

        light_pos = [(l.x, l.y) for l in self.lights]
        light_pos.extend(
            [(0, 0) for _ in range(MAX_LIGHTS - num_lights)])

        light_positions.value = light_pos
