def parse_indents(text, tab_size=4):
    """
    This function parses the indents in a painterly script and inserts the
    necessary close commands based on these indents
    :param text: the text to process
    :param tab_size: an optional number of spaces to use for each tab
    :return: the parsed text
    """
    parsed_text = ''
    previous_line = ''
    indent_stack = [0]
    for line_number, line in enumerate(text.split('\n'), 1):
        deindent_detected = False
        line = line.expandtabs(tab_size)
        if len(line) > 0 and (not line.isspace()):
            num_spaces = len(line) - len(line.lstrip())
            if num_spaces > indent_stack[-1]:
                if not 'sample' in previous_line:
                    raise ValueError(f'Indents are only allowed after sample '
                                     f'commands: at line {line_number}')
                indent_stack.append(num_spaces)

            while num_spaces < indent_stack[-1]:
                deindent_detected = True
                indent_stack.pop()
                parsed_text += ' ' * indent_stack[-1] + ']\n'

            if num_spaces != indent_stack[-1] and deindent_detected:
                raise ValueError(f'Indent error at line {line_number}')
            parsed_text += line + '\n'
            previous_line = line
    return parsed_text
