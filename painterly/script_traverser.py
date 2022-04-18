"""This module traverses a painterly script recursively, crystrallizes all
quantities (including variables), and provides commands with arguments for
later rendering."""

from lark import Tree

import quantity


class ScriptTraverser:
    CLOSE_COMMAND = 'rightbrace'
    SAMPLE_COMMAND = 'sample'
    ASSIGNMENT_COMMAND = 'assignment'
    variables = {}

    def traverse_script(self, commands, level=0, sample_number=0):
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
                arguments = self.crystallize_values(sub_tree.children)
                if instruction_type == self.CLOSE_COMMAND:
                    relative_indent -= 1

                    # yield this function recursively on the
                    # collected commands
                    # within the inner indent
                    if relative_indent == 0:
                        for sample_number_inner in range(
                                num_samples):
                            yield from self.traverse_script(
                                commands[old_index:e],
                                level + 1, sample_number_inner)

                if instruction_type == self.ASSIGNMENT_COMMAND:
                    variable_name = sub_tree.children[0].label
                    value = arguments[0].value
                    quantity.variables[variable_name] = value

                if relative_indent == 0:
                    yield [sample_number, level, instruction_type,
                           arguments]

                if instruction_type == self.SAMPLE_COMMAND:
                    if relative_indent == 0:
                        num_samples = int(arguments[0].value + 0.5)
                        old_index = e + 1
                    relative_indent += 1

    def crystallize_values(self, arguments):
        """
        Instantiates the Value objects into actual floating point values.
        :param arguments: the arguments to process
        :return: the processed arguments with Value objects
                turned into floating point numbers
        """
        instantiated_values = []
        for argument in arguments[1:]:
            if argument:
                instantiated_values.append(argument.value)
            else:
                instantiated_values.append(None)

        return instantiated_values
