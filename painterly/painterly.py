"""This module is the main entry to the painterly library.
This library simulates Chinese style paintings with
distance-based lighting from a custom recursive language"""
from lark import Lark

from script_preprocessor import ScriptPreprocessor
from script_traverser import ScriptTraverser


def main():
    with open('grammar/grammar.ebnf', 'r') as file:
        grammar = file.read()

    parser = Lark(grammar)

    with open('examples/example1.pnt', 'r') as file:
        text = file.read()
    results = parser.parse(text)

    transformer = ScriptPreprocessor()
    transformed_results = transformer.transform(results)

    # initialize a context
    # This will hold the OpenGL buffer, window, shader, brush,
    # and current sampler used for transforms
    # opengl_ctx = openglContext()

    # command_processor = CommandProcessor(opengl_ctx)
    # here we iterate through the transformed tree recursively
    # calling bracketed statement groups
    # we start with 1 sample from the root node
    script_traverser = ScriptTraverser()
    # traverse recursively through the painterly script
    for sample_number, command, arguments in script_traverser.preprocess_script(
            transformed_results.children):
        print(sample_number, command, arguments)

    # script_traverser.process_command_group(transformed_results.children, 0)


if __name__ == '__main__':
    main()
