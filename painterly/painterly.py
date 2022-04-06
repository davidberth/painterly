"""This module is the main entry to the painterly library.  This library simulates
Chinese style paintings with from distance-based lighting from a custom recursive language"""

import moderngl
from PIL import Image

import grammar
import stroke

OUT_FILE = r'output\output.png'
SCALING_FACTOR = 2
SIZE = (1800, 1200)


def main():
    buffer_size = (SIZE[0] * SCALING_FACTOR, SIZE[1] * SCALING_FACTOR)
    ctx = moderngl.create_context(standalone=True)
    # generate the fractal noise texture
    stroke.init(ctx)

    fbo = ctx.simple_framebuffer(buffer_size, components=4)
    fbo.use()
    fbo.clear(1.0, 1.0, 1.0, 1.0)

    with open("shaders/vertex.glsl", "r", encoding="utf-8") as vertex_shader_file:
        vertex_shader = vertex_shader_file.read()
    with open("shaders/fragment.glsl", "r", encoding="utf-8") as fragment_shader_file:
        fragment_shader = fragment_shader_file.read()

    shader = ctx.program(vertex_shader=vertex_shader,
                         fragment_shader=fragment_shader)
    ctx.enable(moderngl.BLEND)

    grammar.setup_grammar(ctx, shader)

    # clean up the context
    ctx.finish()

    # save the buffer to an image file and resize if needed for antialiasing
    image = Image.frombytes('RGBA', buffer_size, fbo.read(components=4))
    if SCALING_FACTOR > 1:
        image = image.resize(SIZE, Image.LANCZOS)
    image = image.transpose(Image.FLIP_TOP_BOTTOM)
    image.save(OUT_FILE, format='png')


if __name__ == '__main__':
    main()
