from lark import Transformer

import quantity


class ScriptPreprocessor(Transformer):
    def __init__(self):
        super().__init__()

    def brushvalue(self, tree):
        tree[0].children[0].label = tree[0].data
        return tree[0].children[0]

    def curve(self, tree):
        tree[0].label = 'curve'
        return tree[0]

    def wavy(self, tree):
        tree[0].label = 'wavy'
        return tree[0]

    def variable(self, tree):
        variable = quantity.Value(0.0, 0.0, quantity.ValueType.variable)
        variable.label = tree[0]
        return variable

    def value(self, tree):

        if isinstance(tree[0], quantity.Value):
            # we already have a value object
            return tree[0]

        if len(tree) == 1:
            # we have a single value
            return quantity.Value(tree[0].value, 0.0,
                                  quantity.ValueType.real)
        else:
            # we have a random distribution to sample from

            value1 = float(tree[0].value)
            value2 = float(tree[1].value)

            value = quantity.Value(value1, value2,
                                   quantity.ValueType.uniform)
            return value
