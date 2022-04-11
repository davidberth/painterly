import numpy as np
from perlin_numpy import generate_fractal_noise_2d
import moderngl


class OpenglContext:
    def __init__(self):
        self.opengl_buffer = None
        self.shader = None
        self.fbo = None
        self.ctx = None

    def init(self, width, height, scaling_factor):
        # here we set up the OpenGL context and canvas
        self.target_size = width, height
        self.scaling_factor = scaling_factor

        self.buffer_size = (
            self.target_size[0] * self.scaling_factor,
            self.target_size[1] * self.scaling_factor)
        self.ctx = moderngl.create_context(standalone=True)

        self.fbo = self.ctx.simple_framebuffer(
            self.buffer_size, components=4)
        self.fbo.use()
        self.fbo.clear(0.8, 0.8, 0.8, 1.0)

        # generate the fractal noise texture
        self.init_perlin()

        with open("shaders/vertex.glsl", "r",
                  encoding="utf-8") as vertex_shader_file:
            vertex_shader = vertex_shader_file.read()
        with open("shaders/fragment.glsl", "r",
                  encoding="utf-8") as fragment_shader_file:
            fragment_shader = fragment_shader_file.read()

        self.shader = self.ctx.program(vertex_shader=vertex_shader,
                                       fragment_shader=fragment_shader)
        self.ctx.enable(moderngl.BLEND)

    def init_perlin(self):
        np.random.seed(0)
        print('generating noise')
        noise_texture = generate_fractal_noise_2d((256, 256), (8, 8), 5).astype(
            np.float32)
        # normalize to 0 .. 1
        noise_texture = (noise_texture + 1.0) / 2.0
        print(' done')

        self.texture = self.ctx.texture([256, 256], 1, noise_texture.tobytes(),
                                        dtype='f4')
        self.texture.filter = (moderngl.LINEAR, moderngl.LINEAR)
