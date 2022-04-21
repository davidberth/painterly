import colorsys

import moderngl
import numpy as np

from brush import Brush

noise_texture = None
texture = None
height_texture_scale = 0.2
length_texture_scale = 2.0


def do_stroke(opengl_ctx, coords, brush: Brush):
    width = brush.thick

    hue = brush.hue
    sat = brush.sat
    bright = brush.bright
    alpha = brush.alpha

    ctx = opengl_ctx.ctx
    shader = opengl_ctx.brush_shader

    # TODO these should be looked up beforehand
    noise_color_scale = shader['noise_color_scale']
    noise_color_scale.value = 0.5

    length_distance_scale = shader['length_distance_scale']
    length_distance_scale.value = 2.0 * brush.consistency * 1.6 / width ** .1

    side_distance_scale = shader['side_distance_scale']
    side_distance_scale.value = 80.0 * brush.consistency

    opengl_ctx.texture.use(location=0)

    normalized_direction = np.array((coords[-1][0] - coords[0][0],
                                     coords[-1][1] - coords[0][1]),
                                    dtype=np.float32)

    stroke_distance = np.sqrt(
        normalized_direction[0] ** 2 + normalized_direction[1] ** 2)
    normalized_direction /= stroke_distance
    orthogonal_direction = np.array(
        (-normalized_direction[1], normalized_direction[0]))

    width_factor = width / 1.8
    tex_x_offset = np.random.uniform(0.0, 1.0 - stroke_distance)
    tex_y_offset = np.random.uniform(0.0, 1.0 - width)
    tex_x_end = tex_x_offset + 0.7 * height_texture_scale
    tex_y_end = tex_y_offset + 0.06 * length_texture_scale

    vertex_list = []

    for e, (x, y) in enumerate(coords):

        if e < len(coords) - 1:
            x2, y2 = coords[e + 1]
            normalized_direction = x2 - x, y2 - y
            stroke_distance = np.sqrt(
                normalized_direction[0] ** 2 + normalized_direction[1] ** 2)
            normalized_direction /= stroke_distance
            orthogonal_direction = np.array(
                (-normalized_direction[1], normalized_direction[0]))

        t = e / float(len(coords) - 1)
        tex_x = tex_x_offset * (1 - t) + tex_x_end * t
        lx1, ly1 = x - orthogonal_direction[0] * width_factor, \
                   y - orthogonal_direction[1] * width_factor

        lx2, ly2 = x + orthogonal_direction[0] * width_factor, \
                   y + orthogonal_direction[1] * width_factor

        red, green, blue = colorsys.hsv_to_rgb(hue, sat,
                                               bright)

        vertex_list.append(
            [lx1, ly1, red, green, blue, alpha, tex_x, tex_y_offset, t,
             0.0])
        vertex_list.append(
            [lx2, ly2, red, green, blue, alpha, tex_x, tex_y_end, t, 1.0])

    vertices = np.array(vertex_list, dtype='f4')

    vao = ctx.vertex_array(shader, ctx.buffer(vertices),
                           'in_vert',
                           'in_color',
                           'in_tex_coord',
                           'in_stroke_coord')
    vao.render(mode=moderngl.TRIANGLE_STRIP)
