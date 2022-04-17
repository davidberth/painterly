"""This module is the main entry to the painterly library.
This library simulates Chinese style paintings with
distance-based lighting from a custom recursive language"""
from lark import Lark

import indent_parser
from command_processor import CommandProcessor
from opengl_context import OpenglContext
from script_preprocessor import ScriptPreprocessor
from script_traverser import ScriptTraverser


def main():
    with open('grammar/grammar.ebnf', 'r') as file:
        grammar = file.read()

    parser = Lark(grammar)

    with open('examples/example1.pnt', 'r') as file:
        text = file.read()

    text = indent_parser.parse_indents(text)
    print('indent processed script')
    print('-----------------------')
    print(text)
    print('-----------------------')
    results = parser.parse(text)

    transformer = ScriptPreprocessor()
    transformed_results = transformer.transform(results)

    # initialize a context
    # This will hold the OpenGL buffer, window, shader, brush,
    # and current sampler used for transforms
    opengl_ctx = OpenglContext()

    command_proc = CommandProcessor(opengl_ctx)
    # here we iterate through the transformed tree recursively
    # calling bracketed statement groups
    # we start with 1 sample from the root node
    script_traverser = ScriptTraverser()
    # traverse recursively through the painterly script and process each
    # command
    for sample_number, level, command, arguments in \
            script_traverser.traverse_script(
                transformed_results.children):
        command_proc.set_sample_number(sample_number)

        getattr(command_proc, command)(arguments)


if __name__ == '__main__':
    main()
