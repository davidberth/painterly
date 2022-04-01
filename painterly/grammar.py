from lark import Lark, Transformer
from stroke import do_stroke
import numpy as np

def setup_grammar(ctx, shader):
    # read the grammar file
    with open('grammar/grammar.ebnf', 'r') as file:
        grammar = file.read()

    parser = Lark(grammar)

    with open('examples/example1.pnt', 'r') as file:
        text = file.read()
    results = parser.parse(text)

    initial_brush = {'hue':0.0, 'sat':0.0, 'bright':0.0, 'alpha':0.9, 'bristle':1.0,
                     'thick':0.005, 'curve':0.0, 'rough':0.0, 'wave':0.0, 'consist':0.6}
    visitor = StrokeVisitor(ctx, shader, initial_brush)
    visitor.transform(results)


class StrokeVisitor(Transformer):
    def __init__(self, ctx, shader, initial_brush):
        super().__init__()
        self.ctx = ctx
        self.shader = shader
        self.current_brush = initial_brush
        self.current_stroke = {'wavy':0.0, 'curve':0.0}
        self.current_sample = False
        self.current_transform = [0.0, 0.0]
        self.path_x = []
        self.path_y = []

    def brush(self, tree):
        # here we update the brush dictionary
        # TODO this will likely need to go in a top down visitor instead
        # of the transformer
        for brush_value in tree[1:]:
            self.current_brush[brush_value[0]] = brush_value[1]



    def stroke(self, tree):

        coord1 = tree[1]
        coord2 = tree[2]
        self.current_stroke['x1'] = coord1[0]
        self.current_stroke['y1'] = coord1[1]
        self.current_stroke['x2'] = coord2[0]
        self.current_stroke['y2'] = coord2[1]

        if tree[3] is not None:
            self.current_stroke['curve'] = tree[3].children[0]
        if tree[4] is not None:
            self.current_stroke['wavy'] = tree[4].children[0]

        #TODO replace this with recursion - we need to visit the grammar multiple times for random numbers
        if self.current_sample:
            for x, y in zip(self.path_x, self.path_y):
                self.path_x, self.path_y = do_stroke(self.ctx, self.shader, self.current_stroke, self.current_brush,
                                                     [x,y])
        else:
            self.path_x, self.path_y = do_stroke(self.ctx, self.shader, self.current_stroke, self.current_brush, self.current_transform)

    def sample(self, tree):
        self.current_sample = True

    def brushvalue(self, tree):
        return [tree[0].data, tree[0].children[0]]

    def coordinate(self, tree):
        return tree
    def value(self, tree):
        # should we rely on the length of the subtree here?
        if len(tree) == 1:
            # we have a single value
            return float(tree[0].value)
        else:
            # we have a random distribution to sample from

            distribution = tree[0].data
            value1 = float(tree[1].value)
            value2 = float(tree[2].value)
            if distribution == 'uniform':
                value = np.random.uniform(value1, value2)
                return value
            elif distribution == 'normal':
                value = np.random.normal(value1, value2)
                return value


