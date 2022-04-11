from lark import Transformer

import quantity


class ScriptTransformer(Transformer):
    def __init__(self):
        super().__init__()

    def brushvalue(self, tree):
        return [tree[0].data, tree[0].children[0]]

    def coordinate(self, tree):
        return [tree[0], tree[1]]

    def curve(self, tree):
        return ['curve', tree[0]]

    def wavy(self, tree):
        return ['wavy', tree[0]]

    def value(self, tree):
        # should we rely on the length of the subtree here?
        if len(tree) == 1:
            # we have a single value
            return quantity.Value(tree[0].value, 0.0, quantity.ValueType.real)
        else:
            # we have a random distribution to sample from

            distribution = tree[0].data
            value1 = float(tree[1].value)
            value2 = float(tree[2].value)
            if distribution == 'uniform':
                value = quantity.Value(value1, value2,
                                       quantity.ValueType.uniform)
                return value
            elif distribution == 'normal':
                value = quantity.Value(value1, value2,
                                       quantity.ValueType.normal)
                return value
