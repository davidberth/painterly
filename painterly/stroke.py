import numpy as np
import moderngl

def stroke( ctx, shader, x1, y1, x2, y2, width, red, green, blue, alpha):
    normalized_direction = np.array((y2 - y1, x2 - x1), dtype=np.float32)
    normalized_direction /= np.sqrt(normalized_direction[0] ** 2 + normalized_direction[1] ** 2)
    orthogonal_direction = np.array((-normalized_direction[1], normalized_direction[0]))

    orthoganal_delta = width * orthogonal_direction / 2.0
    py1, px1 = y1 + orthoganal_delta[0], x1 + orthoganal_delta[1]
    py2, px2 = y2 + orthoganal_delta[0], x2 + orthoganal_delta[1]
    py3, px3 = y2 - orthoganal_delta[0], x2 - orthoganal_delta[1]
    py4, px4 = y1 - orthoganal_delta[0], x1 - orthoganal_delta[1]

    vertices = np.array([
     px1,   py1,   red, green, blue,
     px2,   py2,   red, green, blue,
     px3,   py3,   red, green, blue,
     px4,   py4,   red, green, blue,
    ],
    dtype='f4',
    )

    vao = ctx.simple_vertex_array(shader, ctx.buffer(vertices), 'in_vert', 'in_color')
    vao.render(mode=moderngl.TRIANGLE_STRIP)

