#!/usr/bin/env python
# __author__ = "Ronie Martinez"
# __copyright__ = "Copyright 2018-2019, Ronie Martinez"
# __credits__ = ["Ronie Martinez"]
# __maintainer__ = "Ronie Martinez"
# __email__ = "ronmarti18@gmail.com"

'''

def tokenize(data):
    iterable = iter(data)
    buffer = ''
    while True:
        try:
            char = next(iterable)
            if char == '\\':
                if buffer == '\\':
                    yield buffer + char
                    buffer = ''
                    continue
                elif len(buffer):
                    yield buffer
                buffer = char
                try:
                    buffer += next(iterable)
                    if buffer == r'\\':
                        yield buffer
                        buffer = ''
                except StopIteration:
                    break
            elif char.isalpha():
                if len(buffer):
                    if buffer.endswith('}'):
                        yield buffer
                        yield char
                        buffer = ''
                    elif buffer.startswith('\\'):
                        buffer += char
                else:
                    yield char
            elif char.isdigit():
                if len(buffer):
                    yield buffer
                buffer = char
                while True:
                    try:
                        char = next(iterable)
                    except StopIteration:
                        break
                    if char.isspace():
                        yield buffer
                        buffer = ''
                        break
                    elif char.isdigit() or char == '.':
                        buffer += char
                    else:
                        if buffer.endswith('.'):
                            yield buffer[:-1]
                            yield buffer[-1]
                        else:
                            yield buffer
                        buffer = ''
                        if char == '\\':
                            buffer = char
                        else:
                            yield char
                        break
            elif char.isspace():
                if len(buffer):
                    yield buffer
                    buffer = ''
            elif char in '{}*':
                # FIXME: Anything that starts with '\math' passes. There is a huge list of math symbols in
                #  unimathsymbols.txt and hard-coding all of them is inefficient.
                if buffer.startswith(r'\begin') or buffer.startswith(r'\end') or buffer.startswith(r'\math'):
                    if buffer.endswith('}'):
                        yield buffer
                        yield char
                        buffer = ''
                    else:
                        buffer += char
                else:
                    if len(buffer):
                        yield buffer
                        buffer = ''
                    yield char
            else:
                if len(buffer):
                    yield buffer
                    buffer = ''
                if len(char):
                    yield char
        except StopIteration:
            break
    if len(buffer):
        yield buffer
'''

OPERATORS = "+-*/=()[]_^{}&,"
NO_INCREMENT = 0
INCREMENT = 1

def tokenize(expression_string):
    """Tokenize expression_string."""
    def s_ini():
        """Initial status."""
        if char.isspace():
            yield None, s_ini, INCREMENT
        else:
            buffer.append(char)
            if char.isalpha() or char in OPERATORS:
                yield buffer, s_ini, INCREMENT
            if char == '\\':
                yield  None, s_backslash, INCREMENT
            if char.isdigit() or char in ".,":
                yield  None, s_integer, INCREMENT
            else:
                print(f'---> {char}')

    def s_backslash():
        """Back slash status."""
        buffer.append(char)
        if char in r'\,;':
            yield buffer, s_ini, INCREMENT
        else:
            yield None, s_command, INCREMENT

    def s_command():
        """Command status."""
        if char.isalpha():
            buffer.append(char)
            yield  None, s_command, INCREMENT
        else:
            if ''.join(buffer) in (r"\begin", r"\end",
                                   r"\mathbb"): # Is not a good thingth ;-)
                buffer.append(char)
                yield  None, s_beginend, INCREMENT
            elif ''.join(buffer) in (r"\text"):
                yield  buffer, s_text, INCREMENT
            else:
                yield buffer, s_ini, NO_INCREMENT

    def s_integer():
        """Command number."""
        if char.isdigit():
            buffer.append(char)
            yield  None, s_integer, INCREMENT
        elif char in ".":
            buffer.append(char)
            yield None, s_float, INCREMENT
        else:
            yield buffer, s_ini, NO_INCREMENT

    def s_float():
        """Command number."""
        if char.isdigit():
            buffer.append(char)
            yield  None, s_decimal, INCREMENT
        else:
            buffer0, buffer1 = buffer[:-1], buffer[-1:]
            yield buffer0, s_float, NO_INCREMENT
            yield buffer1, s_ini, NO_INCREMENT

    def s_decimal():
        """Command number."""
        if char.isdigit():
            buffer.append(char)
            yield  None, s_decimal, INCREMENT
        elif char in ".":
            buffer.append(char)
            yield buffer, s_float, INCREMENT
        else:
            yield buffer, s_ini, NO_INCREMENT

    def s_beginend():
        """Begin or end."""
        buffer.append(char)
        if char == "}":
            yield buffer, s_ini, INCREMENT
        else:
            yield None, s_beginend, INCREMENT

    def s_text():
        """text."""
        if char == "}":
            yield buffer, s_ini, INCREMENT
        else:
            buffer.append(char)
            yield None, s_text, INCREMENT


    buffer = []
    status = s_ini
    iterable = iter(expression_string)
    is_next = INCREMENT
    while True:
        try:
            if is_next == INCREMENT:
                char = next(iterable)
            for result, new_status, is_next in status():
                if result:
                    yield ''.join(result)
                    buffer = []
            status = new_status
        except StopIteration:
            break
    if buffer:
        yield ''.join(buffer)
