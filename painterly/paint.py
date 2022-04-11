import colorsys

import moderngl
import numpy as np

from brush import Brush

noise_texture = None
texture = None
height_texture_scale = 0.2
length_texture_scale = 2.0


def do_stroke(opengl_ctx, shader, path, brush: Brush, transform):
    # TODO optimize this - don't need to look this up every stroke

    x1 = path['x1'] + transform[0]
    y1 = path['y1'] + transform[1]
    x2 = path['x2'] + transform[0]
    y2 = path['y2'] + transform[1]

    curve = path['curve']
    if curve is None:
        curve = 0.0
    wavy = path['wavy']
    if wavy is None:
        wavy = 0.0

    width = brush.thick
    hue = brush.hue
    sat = brush.sat
    bright = brush.bright
    alpha = brush.alpha

    red, green, blue = colorsys.hsv_to_rgb(hue, sat, bright)

    noise_color_scale = shader['noise_color_scale']
    noise_color_scale.value = brush.consistency

    length_distance_scale = shader['length_distance_scale']
    length_distance_scale.value = 1.0 * 1.6 / width ** .1

    side_distance_scale = shader['side_distance_scale']
    side_distance_scale.value = 40.0

    opengl_ctx.texture.use(location=0)
    normalized_direction = np.array((x2 - x1, y2 - y1), dtype=np.float32)
    stroke_distance = np.sqrt(
        normalized_direction[0] ** 2 + normalized_direction[1] ** 2)
    normalized_direction /= stroke_distance
    orthogonal_direction = np.array(
        (-normalized_direction[1], normalized_direction[0]))

    width_factor = width / 1.5
    tex_x_offset = np.random.uniform(0.0, 1.0 - stroke_distance)
    tex_y_offset = np.random.uniform(0.0, 1.0 - width)
    tex_x_end = tex_x_offset + 0.7 * height_texture_scale
    tex_y_end = tex_y_offset + 0.06 * length_texture_scale

    vertex_list = []
    path_x = []
    path_y = []
    for t in np.arange(0.0, 1.002, 0.04):
        x = x1 * (1.0 - t) + x2 * t
        y = y1 * (1.0 - t) + y2 * t
        tex_x = tex_x_offset * (1 - t) + tex_x_end * t
        path_curve = np.sqrt(
            1 - (t * 2.0 - 1) ** 2) * curve * stroke_distance * 0.5
        path_wave = np.sin(t * 4.0) * wavy * np.random.uniform(0.8, 1.2)
        lx1, ly1 = x - orthogonal_direction[0] * (
                width_factor + path_curve + path_wave), \
                   y - orthogonal_direction[1] * (
                           width_factor + path_curve + path_wave)
        lx2, ly2 = x + orthogonal_direction[0] * (
                width_factor - path_curve - path_wave), \
                   y + orthogonal_direction[1] * (
                           width_factor - path_curve - path_wave)
        vertex_list.append(
            [lx1, ly1, red, green, blue, alpha, tex_x, tex_y_offset, t, 0.0])
        vertex_list.append(
            [lx2, ly2, red, green, blue, alpha, tex_x, tex_y_end, t, 1.0])

        path_x.append((lx1 + lx2) / 2)
        path_y.append((ly1 + ly2) / 2)

    vertices = np.array(vertex_list, dtype='f4')

    vao = opengl_ctx.ctx.vertex_array(shader, opengl_ctx.ctx.buffer(vertices),
                                      'in_vert',
                                      'in_color',
                                      'in_tex_coord',
                                      'in_stroke_coord')
    vao.render(mode=moderngl.TRIANGLE_STRIP)

    return path_x, path_y
