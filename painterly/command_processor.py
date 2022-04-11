"""
This module contains functions to process each of the painterly commands.
"""
from PIL import Image

import paint
from sampler import Sampler


class CommandProcessor:
    def __init__(self, opengl_ctx):
        self.opengl_ctx = opengl_ctx

    def canvas(self, arguments, brush_ctx):
        """
        Initializes the OpenGL window with the canvas size and antialiasing factor
        :param arguments: the arguments from the painterly command
        """

        width = int(arguments[0])
        height = int(arguments[1])
        scaling_factor = int(arguments[2])
        self.opengl_ctx.init(width, height, scaling_factor)

    def save(self, arguments, brush_ctx):
        # clean up the context
        name = arguments[0]
        self.opengl_ctx.ctx.finish()

        # save the buffer to an image file and resize if needed for antialiasing
        image = Image.frombytes('RGBA', self.opengl_ctx.buffer_size,
                                self.opengl_ctx.fbo.read(components=4))
        if self.opengl_ctx.scaling_factor > 1:
            image = image.resize(self.opengl_ctx.target_size, Image.ANTIALIAS)
        image = image.transpose(Image.FLIP_TOP_BOTTOM)
        image.save(f'output/{name}.png', format='png')

    def brush(self, arguments, brush_ctx):
        """
        Changes the characteristics of the current brush
        :param arguments: the arguments from the painterly command
        :param ctx: the current contex
        """
        for attribute in arguments:
            setattr(brush_ctx.brush, attribute[0], attribute[1])

    def stroke(self, arguments, brush_ctx):
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
            transform = brush_ctx.sampler.get_coord(
                brush_ctx.sample_number)

        brush_ctx.set_path_coords(
            paint.do_stroke(self.opengl_ctx, self.opengl_ctx.shader, path,
                            brush_ctx.brush,
                            transform))

    def sample(self, arguments, brush_ctx):
        """
        Sets the current sampler object to the provided sampler type.
        :param arguments: the arguments from the painterly command
        """
        brush_ctx.num_samples = int(arguments[0] + 0.5)
        brush_ctx.sampler = Sampler(brush_ctx.path_coords,
                                    brush_ctx.num_samples)
