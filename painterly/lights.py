"""
This module keeps track of the set of lights for each layer.
"""

import colorsys

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
        light_intensities = shader['light_intensities']
        light_radii = shader['light_radii']

        light_pos = [(l.x, l.y) for l in self.lights]
        light_pos.extend(
            [(0, 0) for _ in range(MAX_LIGHTS - num_lights)])

        light_int = []
        for l in self.lights:
            red, green, blue = colorsys.hsv_to_rgb(l.hue,
                                                   l.sat,
                                                   l.bright)
            light_int.append((red, green, blue))
        light_int.extend(
            [(0, 0, 0) for _ in range(MAX_LIGHTS - num_lights)])

        light_rad = [l.radius for l in self.lights]
        light_rad.extend([0 for _ in range(MAX_LIGHTS - num_lights)])

        light_positions.value = light_pos
        light_intensities.value = light_int
        light_radii.value = light_rad
