"""This module parses the painterly language, traverses the grammar tree, and
processes each command recursively."""

from lark import Lark, Tree

import command_processor
import opengl_context
import quantity
from script_transformer import ScriptTransformer


class ScriptTraverser:

    def setup_grammar(self):
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

        transformer = ScriptTransformer()
        transformed_results = transformer.transform(results)

        # initialize a context
        # This will hold the OpenGL buffer, window, shader, brush,
        # and current sampler used for transforms
        opengl_ctx = opengl_context.OpenglContext()

        self.command_processor = command_processor.CommandProcessor(opengl_ctx)
        # here we iterate through the transformed tree recursively
        # calling bracketed statement groups
        # we start with 1 sample from the root node
        self.process_command_group(transformed_results.children, 0)

    def process_command_group(self, commands, level):
        """
        This function is recursively called to process the commands in the input
        painterly script.
        :param commands: the list of commands to process at this level
        :param level: the current indentation level
        """
        old_index = 99999
        relative_indent = 0

        self.command_processor.brush_stack.push()

        for e, instruction in enumerate(commands):
            sub_tree = instruction.children[0]
            if isinstance(sub_tree, Tree):
                instruction_type = sub_tree.data
                arguments = quantity.get_values(sub_tree.children)

                match instruction_type:
                    case 'leftbrace':
                        if relative_indent == 0:
                            old_index = e + 1
                        relative_indent += 1

                    case 'rightbrace':
                        relative_indent -= 1

                        # call this function recursively on the
                        # collected commands
                        # within the inner indent
                        if relative_indent == 0:
                            for sample in range(
                                    self.command_processor.num_samples):
                                self.command_processor.set_sample_number(sample)
                                self.process_command_group(
                                    commands[old_index:e],
                                    level + 1)

                        self.command_processor.set_sample_number(0)
                    case _:
                        if relative_indent == 0:
                            # call the command
                            getattr(self.command_processor, instruction_type)(
                                arguments)
        self.command_processor.brush_stack.pop()
