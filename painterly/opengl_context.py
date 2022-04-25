import moderngl
import numpy as np
from perlin_numpy import generate_fractal_noise_2d


class OpenglContext:
    def __init__(self):
        self.opengl_buffer = None
        self.brush_shader = None
        self.pointlight_shader = None
        self.fbo = None
        self.ctx = None
        self.aspect_ratio = 1.0
        self.light_texture = None

    def init(self, width, height, scaling_factor, red, green, blue):
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
        self.fbo.clear(red, green, blue, 1.0, depth=100.0)

        # generate the fractal noise texture
        self.init_perlin()

        with open("shaders/brush_vertex.glsl", "r",
                  encoding="utf-8") as vertex_shader_file:
            vertex_shader = vertex_shader_file.read()
        with open("shaders/brush_fragment.glsl", "r",
                  encoding="utf-8") as fragment_shader_file:
            fragment_shader = fragment_shader_file.read()

        self.brush_shader = self.ctx.program(vertex_shader=vertex_shader,
                                             fragment_shader=fragment_shader)

        self.aspect_ratio = width / height
        self.ctx.enable(moderngl.BLEND)
        self.ctx.enable(moderngl.DEPTH_TEST)

    def init_perlin(self):
        print('generating noise')
        noise_texture = generate_fractal_noise_2d((256, 256), (8, 8), 5).astype(
            np.float32)
        # normalize to 0 .. 1
        noise_texture = (noise_texture + 1.0) / 2.0
        print(' done')

        self.texture = self.ctx.texture([256, 256], 1, noise_texture.tobytes(),
                                        dtype='f4')
        self.texture.filter = (moderngl.LINEAR, moderngl.LINEAR)
