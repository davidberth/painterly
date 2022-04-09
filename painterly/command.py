"""
This module contains functions to process each of the painterly commands.
"""
import moderngl
from PIL import Image

import paint
from sampler import Sampler


def canvas(arguments, ctx):
    """
    Initializes the OpenGL window with the canvas size and antialiasing factor
    :param arguments: the arguments from the painterly command
    :param ctx: the current contex
    """

    # here we set up the OpenGL context and canvas
    ctx.target_size = int(arguments[0]), int(arguments[1])
    ctx.scaling_factor = int(arguments[2])

    ctx.buffer_size = (
        ctx.target_size[0] * ctx.scaling_factor, ctx.target_size[1] * ctx.scaling_factor)
    ctx.opengl_ctx = moderngl.create_context(standalone=True)
    # generate the fractal noise texture

    ctx.fbo = ctx.opengl_ctx.simple_framebuffer(ctx.buffer_size, components=4)
    ctx.fbo.use()
    ctx.fbo.clear(0.8, 0.8, 0.8, 1.0)

    paint.init(ctx.opengl_ctx)

    with open("shaders/vertex.glsl", "r", encoding="utf-8") as vertex_shader_file:
        vertex_shader = vertex_shader_file.read()
    with open("shaders/fragment.glsl", "r", encoding="utf-8") as fragment_shader_file:
        fragment_shader = fragment_shader_file.read()

    ctx.shader = ctx.opengl_ctx.program(vertex_shader=vertex_shader,
                                        fragment_shader=fragment_shader)
    ctx.opengl_ctx.enable(moderngl.BLEND)


def save(arguments, ctx):
    # clean up the context
    name = arguments[0]
    ctx.opengl_ctx.finish()

    # save the buffer to an image file and resize if needed for antialiasing
    image = Image.frombytes('RGBA', ctx.buffer_size, ctx.fbo.read(components=4))
    if ctx.scaling_factor > 1:
        image = image.resize(ctx.target_size, Image.ANTIALIAS)
    image = image.transpose(Image.FLIP_TOP_BOTTOM)
    image.save(f'output/{name}.png', format='png')


def brush(arguments, ctx):
    """
    Changes the characteristics of the current brush
    :param arguments: the arguments from the painterly command
    :param ctx: the current contex
    """
    for attribute in arguments:
        setattr(ctx.brush, attribute[0], attribute[1])


def stroke(arguments, ctx):
    """
    Performs a brush stroke at the provided coordinates and with
    the given curve and wavy values.
    :param arguments: the arguments from the painterly command
    :param ctx: the current contex
    """
    # TODO we need a stroke or path class
    x1, y1 = arguments[0]
    x2, y2 = arguments[1]
    path = dict()
    path['x1'] = x1
    path['x2'] = x2
    path['y1'] = y1
    path['y2'] = y2
    path['wavy'] = None
    path['curve'] = None
    if len(arguments) > 2:
        path[arguments[2][0]] = arguments[2][1]
    if len(arguments) > 3:
        path[arguments[3][0]] = arguments[3][1]

    if ctx.sampler is None:
        transform = [0.0, 0.0]
    else:
        transform = ctx.sampler.get_coord(ctx.sample_number)

    ctx.set_last_coords(paint.do_stroke(ctx.opengl_ctx, ctx.shader, path, ctx.brush, transform))


def sample(arguments, ctx):
    """
    Sets the current sampler object to the provided sampler type.
    :param arguments: the arguments from the painterly command
    :param ctx: the current context
    """
    ctx.num_samples = int(arguments[0] + 0.5)
    ctx.set_sampler(Sampler(ctx.last_coord, ctx.num_samples))
