"""
This module implements point lights.
"""
import colorsys
from dataclasses import dataclass

import moderngl
import numpy as np


@dataclass
class Light:
    x: float = 0.0
    y: float = 0.0
    hue: float = 0.0
    sat: float = 0.0
    bright: float = 0.0
    radius: float = 0.0
    falloff: float = 1.0

    def render(self, ctx):
        red, green, blue = colorsys.hsv_to_rgb(self.hue,
                                               self.sat,
                                               self.bright)

        vertex_list = [
            [self.x - 0.02, self.y - 0.04, red, green, blue, 0.15, -1.0, -1.0],
            [self.x - 0.02, self.y + 0.04, red, green, blue, 0.15, -1.0, 1.0],
            [self.x + 0.02, self.y - 0.04, red, green, blue, 0.15, 1.0, -1.0],
            [self.x + 0.02, self.y + 0.04, red, green, blue, 0.15, 1.0, 1.0]]

        vertices = np.array(vertex_list, dtype='f4')

        vao = ctx.ctx.vertex_array(ctx.pointlight_shader,
                                   ctx.ctx.buffer(vertices),
                                   'in_vert',
                                   'in_color',
                                   'in_tex_coord')

        vao.render(mode=moderngl.TRIANGLE_STRIP)
