"""
This module keeps track of the set of lights for each layer.
"""

import colorsys

import moderngl
import numpy as np

from light import Light

MAX_LIGHTS = 512


class Lights:
    lights = []
    texture = None

    def add_light(self, x, y, hue, sat, bright, alpha, radius):
        self.lights.append(Light(x, y, hue, sat, bright, alpha, radius))

    def create_texture(self, opengl_ctx):
        shader = opengl_ctx.brush_shader
        num_lights = len(self.lights)
        shader['num_lights'].value = num_lights

        self.matrix = np.zeros((8, 2048, 3), dtype=np.float32)

        for e, l in enumerate(self.lights):
            red, green, blue = colorsys.hsv_to_rgb(l.hue,
                                                   l.sat,
                                                   l.bright)
            self.matrix[0, e, :2] = (l.x, l.y)
            self.matrix[1, e, :] = (red, green, blue)
            self.matrix[2, e, 0] = l.radius

        opengl_ctx.light_texture = opengl_ctx.ctx.texture(
            (2048, 8), 3,
            self.matrix.tobytes(), dtype='f4')

        opengl_ctx.light_texture.filter = (moderngl.NEAREST, moderngl.NEAREST)
        # enable this texture
        opengl_ctx.light_texture.use(location=1)
        shader['noise_texture'].value = 0
        shader['lights_texture'].value = 1
