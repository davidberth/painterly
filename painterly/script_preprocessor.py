from lark import Transformer

import quantity


class ScriptPreprocessor(Transformer):
    def __init__(self):
        super().__init__()

    def brushvalue(self, tree):
        tree[0].children[0].tag = tree[0].data
        return tree[0].children[0]

    def samplervalue(self, tree):
        tree[0].children[0].tag = tree[0].data
        return tree[0].children[0]

    def curve(self, tree):
        tree[0].tag = 'curve'
        return tree[0]

    def wavy(self, tree):
        tree[0].tag = 'wavy'
        return tree[0]

    def variable(self, tree):
        variable = quantity.Value(0.0, 0.0, quantity.ValueType.variable)
        variable.name = tree[0]
        return variable

    def value(self, tree):

        if isinstance(tree[0], quantity.Value):
            # we already have a value object
            # this should be a variable

            # if it has a multiplier, we set this in the value object
            if len(tree) == 2:
                if tree[1] is not None:
                    tree[0].multiplier = float(tree[1].children[0].value)
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
