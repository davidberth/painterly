"""
This module contains functions to process each of the painterly commands.
"""
import moderngl
from PIL import Image

import paint
from sampler import Sampler


def canvas(arguments, opengl_ctx, brush_ctx):
    """
    Initializes the OpenGL window with the canvas size and antialiasing factor
    :param arguments: the arguments from the painterly command
    :param opengl_ctx: the current Opengl context
    :param stack: the current Brush context
    """

    width = int(arguments[0])
    height = int(arguments[1])
    scaling_factor = int(arguments[2])
    opengl_ctx.init(width, height, scaling_factor)


def save(arguments, opengl_ctx, brush_ctx):
    # clean up the context
    name = arguments[0]
    opengl_ctx.ctx.finish()

    # save the buffer to an image file and resize if needed for antialiasing
    image = Image.frombytes('RGBA', opengl_ctx.buffer_size,
                            opengl_ctx.fbo.read(components=4))
    if opengl_ctx.scaling_factor > 1:
        image = image.resize(opengl_ctx.target_size, Image.ANTIALIAS)
    image = image.transpose(Image.FLIP_TOP_BOTTOM)
    image.save(f'output/{name}.png', format='png')


def brush(arguments, opengl_ctx, brush_ctx):
    """
    Changes the characteristics of the current brush
    :param arguments: the arguments from the painterly command
    :param ctx: the current contex
    """
    for attribute in arguments:
        setattr(brush_ctx.brush, attribute[0], attribute[1])


def stroke(arguments, opengl_ctx, brush_ctx):
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

    if brush_ctx.sampler is None:
        transform = [0.0, 0.0]
    else:
        transform = brush_ctx.sampler.get_coord(brush_ctx.sample_number)

    brush_ctx.set_path_coords(
        paint.do_stroke(opengl_ctx, opengl_ctx.shader, path,
                        brush_ctx.brush,
                        transform))


def sample(arguments, opengl_ctx, brush_ctx):
    """
    Sets the current sampler object to the provided sampler type.
    :param arguments: the arguments from the painterly command
    :param ctx: the current context
    """
    brush_ctx.num_samples = int(arguments[0] + 0.5)
    brush_ctx.sampler = Sampler(brush_ctx.path_coords, brush_ctx.num_samples)
