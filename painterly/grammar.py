"""This module parses the painterly language, traverses the grammar tree, and
processes each command recursively."""

from lark import Lark, Transformer, Token, Tree

import command
import context
import quantity
from brush import Brush


def setup_grammar():
    """
    This function reads the grammar file and initializes the parser
    """
    # read the grammar file
    with open('grammar/grammar.ebnf', 'r') as file:
        grammar = file.read()

    parser = Lark(grammar)

    with open('examples/example1.pnt', 'r') as file:
        text = file.read()
    results = parser.parse(text)

    transformer = StrokeTransformer()
    transformed_results = transformer.transform(results)

    # initialize a context
    # This will hold the OpenGL buffer, window, shader, brush,
    # and current sampler used for transforms
    ctx = context.Context()
    brush = Brush()
    ctx.add_brush(brush)

    # here we iterate through the transformed tree recursively calling bracketed statement groups
    # we start with 1 sample from the root node
    process_command_group(transformed_results.children, ctx, 0)


def process_command_group(commands, ctx, level):
    """
    This function is recursively called to process the commands in the input painterly script.
    :param commands: the list of commands to process at this level
    :param level: the current indentation level
    """
    old_index = 99999
    relative_indent = 0

    ctx.push_sampler()
    ctx.push_brush()
    for e, instruction in enumerate(commands):
        sub_tree = instruction.children[0]
        if isinstance(sub_tree, Tree):
            instruction_type = sub_tree.data
            arguments = get_values(sub_tree.children)

            match instruction_type:
                case 'leftbrace':
                    if relative_indent == 0:
                        old_index = e + 1
                    relative_indent += 1

                case 'rightbrace':
                    relative_indent -= 1

                    # call this function recursively on the collected commands within the inner indent
                    if relative_indent == 0:
                        for sample in range(ctx.num_samples):
                            ctx.sample_number = sample
                            process_command_group(commands[old_index:e], ctx, level + 1)

                    ctx.sample_number = 0
                case _:
                    if relative_indent == 0:
                        # call the command
                        getattr(command, instruction_type)(arguments, ctx)
    ctx.pop_sampler()
    ctx.pop_brush()


def get_values(arguments):
    """
    Instantiates the Value objects into actual floating point values.
    :param arguments: the arguments to process
    :return: the processed arguments with Value objects turned into floating point numbers
    """
    realized = []
    for argument in arguments[1:]:

        if isinstance(argument, list):
            realized_argument = []
            for component in argument:
                if isinstance(component, quantity.Value):
                    # crystallize the random value
                    realized_argument.append(component.value)
                else:
                    realized_argument.append(component)
            realized.append(realized_argument)
        else:
            if isinstance(argument, quantity.Value):
                realized.append(argument.value)
            elif isinstance(argument, Token):
                realized.append(argument.value)

    return realized


class StrokeTransformer(Transformer):
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
                value = quantity.Value(value1, value2, quantity.ValueType.uniform)
                return value
            elif distribution == 'normal':
                value = quantity.Value(value1, value2, quantity.ValueType.normal)
                return value
