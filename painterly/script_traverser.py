"""This module parses the painterly language, traverses the grammar tree, and
processes each command recursively."""

from lark import Tree

import quantity


class ScriptTraverser:
    open_command = 'leftbrace'
    close_command = 'rightbrace'
    sample_command = 'sample'

    def preprocess_script(self, commands, level=0, sample_number=0):
        """
        This function is recursively called to traverse a painterly script
        :param commands: the list of commands to process at this level
        :param level: the current indentation level
        :param sample_number: the current sample number
        """
        old_index = 999999
        relative_indent = 0

        for e, instruction in enumerate(commands):
            sub_tree = instruction.children[0]
            if isinstance(sub_tree, Tree):
                instruction_type = sub_tree.data
                arguments = quantity.get_values(sub_tree.children)

                if instruction_type == self.close_command:
                    relative_indent -= 1

                    # call this function recursively on the
                    # collected commands
                    # within the inner indent
                    if relative_indent == 0:
                        for sample_number in range(
                                num_samples):
                            yield from self.preprocess_script(
                                commands[old_index:e],
                                level + 1, sample_number)
                        sample_number = 0

                if relative_indent == 0:
                    yield [sample_number, instruction_type,
                           arguments]

                if instruction_type == self.sample_command:
                    num_samples = int(arguments[0] + 0.5)

                if instruction_type == self.open_command:
                    if relative_indent == 0:
                        old_index = e + 1
                    relative_indent += 1
