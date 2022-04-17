"""
This module contains functions to process each of the painterly commands.
"""
from PIL import Image

import paint
from brush_stack import BrushStack
from sampler import Sampler


class CommandProcessor:
    def __init__(self, opengl_ctx):
        self.opengl_ctx = opengl_ctx
        self.brush_stack = BrushStack()
        self.sample_number = 0

    def set_sample_number(self, sample_number):
        self.sample_number = sample_number

    @property
    def num_samples(self):
        return self.brush_stack.brush_context.num_samples

    def canvas(self, arguments):
        """
        Initializes the OpenGL window with the canvas size and antialiasing
        factor
        :param arguments: the arguments from the painterly command
        """

        width = int(arguments[0])
        height = int(arguments[1])
        scaling_factor = int(arguments[2])
        self.opengl_ctx.init(width, height, scaling_factor)

    def save(self, arguments):
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

    def brush(self, arguments):
        """
        Changes the characteristics of the current brush
        :param arguments: the arguments from the painterly command
        :param ctx: the current contex
        """
        for attribute in arguments:
            setattr(self.brush_stack.brush_context.brush,
                    attribute[0], attribute[1])

    def stroke(self, arguments):
        """
        Performs a brush stroke at the provided coordinates and with
        the given curve and wavy values.
        :param arguments: the arguments from the painterly command
        :param ctx: the current contex
        """
        # TODO we need a stroke or path class

        # for i in self.brush_stack.brush_contexts:
        #    print(i.sampler)

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

        if self.brush_stack.brush_context.sampler is None:
            transform = [0.0, 0.0]
        else:
            transform = self.brush_stack.brush_context.sampler.get_coord(
                self.sample_number)

        self.brush_stack.brush_context.set_path_coords(
            paint.do_stroke(self.opengl_ctx, self.opengl_ctx.shader, path,
                            self.brush_stack.brush_context.brush,
                            transform))

    def sample(self, arguments):
        """
        Sets the current sampler object to the provided sampler type.
        :param arguments: the arguments from the painterly command
        """
        self.brush_stack.push()
        self.brush_stack.brush_context.num_samples = int(arguments[0] + 0.5)
        self.brush_stack.brush_context.sampler = Sampler(
            self.brush_stack.brush_context.path_coords,
            self.brush_stack.brush_context.num_samples)

    def rightbrace(self, arguments):
        self.brush_stack.pop()

    # def push(self, arguments):

    # def pop(self, arguments):
