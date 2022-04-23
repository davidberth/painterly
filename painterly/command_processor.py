"""
This module contains functions to process each of the painterly commands.
"""

from PIL import Image

from brush_stack import BrushStack
from lights import Lights
from path import Path
from sampler import Sampler
from strokes import Strokes


class CommandProcessor:
    def __init__(self, opengl_ctx):
        self.opengl_ctx = opengl_ctx
        self.brush_stack = BrushStack()
        self.sample_number = 0
        self.strokes = Strokes()
        self.lights = Lights()

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

        width = int(arguments[0].value)
        height = int(arguments[1].value)
        scaling_factor = int(arguments[2].value)
        red = arguments[3].value
        green = arguments[4].value
        blue = arguments[5].value
        self.opengl_ctx.init(width, height, scaling_factor, red, green, blue)

    def save(self, arguments):
        # render the scene
        self.strokes.render(self.opengl_ctx)
        self.lights.render(self.opengl_ctx)

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
                    attribute.label, attribute.value)

    def light(self, arguments):

        x = arguments[0].value
        y = arguments[1].value

        if self.brush_stack.brush_context.sampler is not None:
            x, y = self.brush_stack.brush_context.sampler.transform(x, y,
                                                                    self.sample_number)

        self.lights.add_light(x, y,
                              arguments[2].value, arguments[3].value,
                              arguments[4].value, arguments[5].value,
                              arguments[6].value)

    def stroke(self, arguments):
        """
        Performs a brush stroke at the provided coordinates and with
        the given curve and wavy values.
        :param arguments: the arguments from the painterly command
        :param ctx: the current contex
        """

        x1 = arguments[0].value
        y1 = arguments[1].value
        x2 = arguments[2].value
        y2 = arguments[3].value

        if self.brush_stack.brush_context.sampler is not None:
            x1, y1 = self.brush_stack.brush_context.sampler.transform(x1, y1,
                                                                      self.sample_number)
            x2, y2 = self.brush_stack.brush_context.sampler.transform(x2, y2,
                                                                      self.sample_number)

        stroke_path = Path()
        stroke_path.x1 = x1
        stroke_path.y1 = y1
        stroke_path.x2 = x2
        stroke_path.y2 = y2

        if arguments[4] is not None:
            stroke_path.curve = arguments[4].value
        if arguments[5] is not None:
            stroke_path.wavy = arguments[5].value

        path_coords = stroke_path.get_path_vertices()

        self.strokes.add_stroke(path_coords,
                                self.brush_stack.brush_context.brush)

        self.brush_stack.brush_context.set_path_coords(path_coords)

    def sample(self, arguments):
        """
        Sets the current sampler object to the provided sampler type.
        :param arguments: the arguments from the painterly command
        """

        sampler_params = {}
        for argument in arguments[1:]:
            if argument:
                sampler_params[argument.label] = argument.value

        self.brush_stack.push()
        self.brush_stack.brush_context.num_samples = int(
            arguments[0].value + 0.5)
        self.brush_stack.brush_context.sampler = Sampler(
            self.brush_stack.brush_context.path_coords,
            self.brush_stack.brush_context.num_samples,
            **sampler_params)

    def assignment(self, arguments):
        pass

    def rightbrace(self, arguments):
        self.brush_stack.pop()
