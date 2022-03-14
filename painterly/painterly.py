import numpy as np
from PIL import Image
import moderngl
from stroke import stroke, init


out_file = r'output\output.png'
scaling_factor = 4
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
# render the scene
# TODO make these more readable - named arguments?

for y in np.arange(0.05, 0.85, 0.1):
    stroke(ctx, shader, 0.0, y, 1.0, y+ y/5.0, 0.06 - y / 80.0, (1 - y), y, 0.0, 0.99)
for x in np.arange(0.05, 0.85, 0.1):
    stroke(ctx, shader, x, 0.1, x + 0.1, 0.95, 0.06 - x/13.0, 0.1,0.1,0.1, 0.99)

# clean up the context
ctx.finish()

# save the buffer to an image file and resize if needed for antialising
image = Image.frombytes('RGBA', buffer_size, fbo.read(components=4))
if scaling_factor > 1:
    image = image.resize(size, Image.ANTIALIAS)
image = image.transpose(Image.FLIP_TOP_BOTTOM)
image.save(out_file, format='png')
