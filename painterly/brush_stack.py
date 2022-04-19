import copy

import brush_context


class BrushStack:
    def __init__(self):
        # we start with a single brush context in the stack
        self.brush_contexts = [brush_context.BrushContext()]

    @property
    def brush_context(self):
        if len(self.brush_contexts) > 0:
            return self.brush_contexts[-1]
        else:
            return None

    def push(self):
        if len(self.brush_contexts) > 0:
            brush = self.brush_context.brush
            self.brush_contexts.append(copy.deepcopy(self.brush_context))
            self.brush_context.brush = copy.deepcopy(brush)
        else:
            print('push: the stack is currently empty')

    def pop(self):
        if len(self.brush_contexts) > 0:
            self.brush_contexts.pop()
        else:
            print('pop: the stack is currently empty')
