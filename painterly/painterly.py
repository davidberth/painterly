import numpy as np
from PIL import Image
import moderngl
import os

out_file = r'output\triangle.png'
scaling_factor = 1
size = (1600, 1100)

buffer_size = (1024 * scaling_factor, 800 * scaling_factor)

ctx = moderngl.create_context(standalone=True)
fbo = ctx.simple_framebuffer(buffer_size, components=4)
fbo.use()
fbo.clear(1.0, 1.0, 1.0, 1.0)

vertices = np.array([
     1.0,   0.0,   1.0, 0.0, 0.0,
     0.0,   0.0,   1.0, 0.0, 1.0,
     1.0,   1.0,   1.0, 0.0, 0.0,
     0.0,   1.0,   1.0, 0.0, 1.0,
],
    dtype='f4',
)

with open("shaders/vertex.glsl", "r") as vertex_shader_file:
    vertex_shader = vertex_shader_file.read()
with open("shaders/fragment.glsl", "r") as fragment_shader_file:
    fragment_shader = fragment_shader_file.read()


prog = ctx.program(vertex_shader=vertex_shader,
                   fragment_shader=fragment_shader)

ctx.finish()

image = Image.frombytes('RGBA', buffer_size, fbo.read(components=4))
if scaling_factor > 1:
    image = image.resize(size, Image.ANTIALIAS)
image = image.transpose(Image.FLIP_TOP_BOTTOM)
image.save(out_file, format='png')
#os.system(out_file)