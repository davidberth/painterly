import numpy as np
from PIL import Image
import moderngl
from stroke import init
import grammar


def draw_box(ctx, shader, x1, y1, x2, y2, width, red, green, blue, alpha):
    stroke(ctx, shader, x1, y1, x1, y2, width, red, green, blue, alpha)
    stroke(ctx, shader, x1, y2, x2, y2, width, red, green, blue, alpha)
    stroke(ctx, shader, x2, y2, x2, y1, width, red, green, blue, alpha)
    stroke(ctx, shader, x2, y1, x1, y1, width, red, green, blue, alpha)

out_file = r'output\output.png'
scaling_factor = 2
size = (1600, 1100)


buffer_size = (1024 * scaling_factor, 800 * scaling_factor)
ctx = moderngl.create_context(standalone=True)
# generate the fractal noise texture
# TODO reorganize this
init(ctx)

fbo = ctx.simple_framebuffer(buffer_size, components=4)
fbo.use()
fbo.clear(1.0, 1.0, 1.0, 1.0)

with open("shaders/vertex.glsl", "r") as vertex_shader_file:
    vertex_shader = vertex_shader_file.read()
with open("shaders/fragment.glsl", "r") as fragment_shader_file:
    fragment_shader = fragment_shader_file.read()

shader = ctx.program(vertex_shader=vertex_shader,
                   fragment_shader=fragment_shader)
ctx.enable(moderngl.BLEND)

grammar.setup_grammar(ctx, shader)

# clean up the context
ctx.finish()

# save the buffer to an image file and resize if needed for antialising
image = Image.frombytes('RGBA', buffer_size, fbo.read(components=4))
if scaling_factor > 1:
    image = image.resize(size, Image.ANTIALIAS)
image = image.transpose(Image.FLIP_TOP_BOTTOM)
image.save(out_file, format='png')

# Example city scene
#stroke(ctx, shader, 0.0, 0.25, 1.0, 0.25, 0.007, 0.1, 0.1, 0.1, 0.8)
# for x in np.arange(0.1, 0.9, 0.1):
#     height = np.random.uniform(0.1, 0.3)
#     width = np.random.uniform(0.05, 0.08)
#     stroke(ctx, shader, x, 0.25 + height, x + width, 0.25 + height, 0.007, 0.1, 0.1, 0.1, 0.9)
#     stroke(ctx, shader, x, 0.25 + height, x, 0.25, 0.006, 0.1, 0.1, 0.1, 0.95)
#     stroke(ctx, shader, x + width, 0.25 + height, x + width, 0.25, 0.006, 0.1, 0.1, 0.1, 0.96)
#
#     red = np.random.uniform(0.2, 1.0)
#     green = np.random.uniform(0.2, 1.0)
#     blue = np.random.uniform(0.2, 1.0)
#     stroke(ctx, shader, x + width / 2, 0.25 + height, x + width / 2, 0.25, width * 1.1, red, green, blue, 0.4, smoothness = 1.7)
#
#     # generate the windows
#     num_rows = int(height * 30.0)
#     num_cols = int(width * 30.0) + 1
#     for row in range(num_rows):
#         for col in range(num_cols):
#             draw_box(ctx, shader, x + col / 40.0 + 0.005, 0.26 + row / 30.0, x + col / 40.0 + 0.015, 0.26 + row / 30 + 0.01, 0.004, 0.0, 0.0, 0.0, 0.9)
#             if np.random.uniform(0.0, 1.0) > 0.5:
#                 stroke(ctx, shader, x + col / 40.0 + 0.0075, 0.26 + row / 30.0 + 0.01,  x + col / 40.0 + 0.0075, 0.26 + row / 30.0, 0.01, 1.0, 1.0, 0.0, 0.9)

#for y in np.arange(0.05, 0.85, 0.1):
#    stroke(ctx, shader, 0.0, y, 1.0, y+ y/5.0, 0.06 - y / 80.0, (1 - y), y, 0.0, 0.99)
#for x in np.arange(0.05, 0.85, 0.1):
#    stroke(ctx, shader, x, 0.1, x + 0.1, 0.95, 0.06 - x/13.0, 0.1,0.1,0.1, 0.99)