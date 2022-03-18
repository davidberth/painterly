from lark import Lark, Transformer
from stroke import stroke
import numpy as np

def setup_grammar(ctx, shader):
    # read the grammar file
    with open('grammar/grammar.ebnf', 'r') as file:
        grammar = file.read()

    parser = Lark(grammar)

    with open('examples/example1.pnt', 'r') as file:
        text = file.read()
    results = parser.parse(text)

    visitor = StrokeVisitor(ctx, shader)
    visitor.transform(results)


class StrokeVisitor(Transformer):
    def __init__(self, ctx, shader):
        super().__init__()
        self.ctx = ctx
        self.shader = shader
    def stroke(self, tree):

        coord1 = tree[1]
        coord2 = tree[2]
        brush = tree[3].children
        print (coord1, coord2, brush)
        stroke(self.ctx, self.shader, *coord1, *coord2, *brush)

    def coordinate(self, tree):
        return tree
    def value(self, tree):
        # should we rely on the length of the subtree here?
        if len(tree) == 1:
            # we have a single value
            return float(tree[0].value)
        else:
            # we have a random distribution to sample from
            print (tree[0])
            distribution = tree[0].data
            value1 = float(tree[1].value)
            value2 = float(tree[2].value)
            if distribution == 'uniform':
                value = np.random.uniform(value1, value2)
                return value
            elif distribution == 'normal':
                value = np.random.normal(value1, value2)
                return value





#    for instruction in results.children:
#        run_instruction(instruction, ctx, shader)

#def run_instruction(t, ctx, shader):
#    if t.data == 'stroke':
#        _, x1, y1, x2, y2 = t.children
#        x1 = float(x1.value)
#        y1 = float(y1.value)
#        x2 = float(x2.value)
#        y2 = float(y2.value)
#        stroke(ctx, shader, x1, y1, x2, y2, 0.05, 0.01, 0.01, 0.01, 0.9)
#    else:
#        raise SyntaxError('Unknown instruction: %s' % t.data)