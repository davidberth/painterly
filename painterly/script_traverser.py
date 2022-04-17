"""This module parses the painterly language, traverses the grammar tree, and
processes each command recursively."""

from lark import Tree

import quantity


class ScriptTraverser:
    close_command = 'rightbrace'
    sample_command = 'sample'
    num_samples = [1]

    def traverse_script(self, commands, level=0, sample_number=0):
        """
        This function is recursively called to traverse a painterly script
        :param commands: the list of commands to process at this level
        :param level: the current indentation level
        :param sample_number: the current sample number
        """
        old_index = 999999
        relative_indent = 0

        self.num_samples.append(self.num_samples[-1])

        for e, instruction in enumerate(commands):
            sub_tree = instruction.children[0]
            if isinstance(sub_tree, Tree):
                instruction_type = sub_tree.data
                arguments = quantity.get_values(sub_tree.children)

                if instruction_type == self.close_command:
                    relative_indent -= 1

                    # yield this function recursively on the
                    # collected commands
                    # within the inner indent
                    if relative_indent == 0:
                        for sample_number_inner in range(
                                self.num_samples[-1]):
                            yield from self.traverse_script(
                                commands[old_index:e],
                                level + 1, sample_number_inner)

                if relative_indent == 0:
                    yield [sample_number, level, instruction_type,
                           arguments]

                if instruction_type == self.sample_command:
                    if relative_indent == 0:
                        self.num_samples[-1] = int(arguments[0] + 0.5)
                        old_index = e + 1
                    relative_indent += 1

        self.num_samples.pop()
