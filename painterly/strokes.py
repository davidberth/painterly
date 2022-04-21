"""
This class represents a set of paint strokes (paths and brushes).  We use
defered rendering to be able to handle specifying lights in arbitrary order,
layers, and z-orders.
"""
import copy

import render


class Strokes:
    strokes = []
    num_strokes = 0

    def add_stroke(self, stroke_path, brush):
        self.strokes.append((stroke_path, copy.copy(brush)))
        self.num_strokes = len(self.strokes)

    def render(self, opengl_context, lights):
        for i in self.strokes:
            render.do_stroke(opengl_context, i[0], i[1], 0.4, lights)
