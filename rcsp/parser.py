"""
Parser for a simple CSP language.

Copyright (C) Sarah Mount, 2013.

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

# pylint: disable=W0602
# pylint: disable=W0232

try:
    from rpython.rlib import rstring
#    from rpython.rlib.objectmodel import specialize
except ImportError:
    pass
    # class specialize:
    #     def memo(self, func):
    #         return func
    # specialize = specialize()

__date__ = 'August 2013'
__author__ = 'Sarah Mount <s.mount@wlv.ac.uk>'

# Set this switch to True to run this interpreter with CPython.
# Set this switch to False to compile this interpreter with rpython.
# Now changed automatically by the 'test' and 'translate' scripts.
DEBUG = False

OPCODES = {
    # Integer arithmetic.
    'ADD': 0, 'MINUS': 1, 'TIMES': 2, 'DIV': 3, 'MOD': 4,
    # Integer comparisons.
    'GT': 5, 'LT': 6, 'EQ': 7, 'NEQ': 8, 'GEQ': 9, 'LEQ': 10,
    # I/O.
    'PRINT_ITEM': 11, 'PRINT_NEWLINE': 12,
    # Global variables.
    'STORE': 13, 'LOAD_GLOBAL': 14, 'LOAD_CONST': 15, 'LOAD_NAME': 16,
    # Control flow.
    'JUMP_FORWARD': 17, 'POP_JUMP_IF_TRUE': 18, 'POP_JUMP_IF_FALSE': 19,
    'JUMP_ABSOLUTE': 20,
    # Function creation and calls.
    'CALL_FUNCTION': 21,
    'LOAD_ARG': 22,
    # Future-proofing...
    'MAKE_FUNCTION': 23,
    'RETURN': 24,
}


def opcode(name):
    return OPCODES[name]


def opcode_mnemonics():
    return OPCODES.keys()


def opcode_values():
    return OPCODES.values()


def parse_bytecode_file(bytecode_file):
    """Parse a file of bytecode.
    The argument should be the text of the original file, with
    mnemonic bytecodes. The result will be a code object.
    """
    from rcsp.box import CodeBox, ProgramBox
    bytecode = []
    # Split bytecode into individual strings.
    # Throw away comments and whitespace.
    for line_ in bytecode_file.split('\n'):
        if DEBUG:
            line = line_.strip()
        else:
            line = rstring.strip_spaces(line_)
        if line.startswith('#'):
            continue
        else:
            if DEBUG:
                for code in line.split():
                    bytecode.append(code)
            else:
                bytecode.extend(rstring.split(line))
    # Parse bytecodes into numeric opcodes.
    # codes included here for future-proofing.
    functions = {}  # Dict of str names -> CodeBox objects
    counter = 0
    while counter < len(bytecode):
        opcodes, strings, integers, bools = [], [], [], []
        name = ''  # Name of each function which is parsed.
        code = bytecode[counter]
        # Parse a list of functions.
        if code == 'DEF':
            counter += 1  # Skip DEF.
            name = bytecode[counter]
            counter += 1  # Skip name of function.
            code = bytecode[counter]
            # TODO: Enable nested functions.
            while code != 'ENDDEF':
                # Handle general instructions.
                if code in opcode_mnemonics():
                    opcodes.append(opcode(code))
                # Handle literals.
                else:
                    if code.isdigit():
                        integers.append(int(code))
                        opcodes.append(len(integers) - 1)
                    elif code == 'True' or code == 'False':
                        bools.append(bool(code))
                        opcodes.append(len(bools) - 1)
                    else:
                        strings.append(code)
                        opcodes.append(len(strings) - 1)
                counter += 1
                code = bytecode[counter]
            # codes_ is an empty list since we don't yet have nested fns.
            functions[name] = CodeBox(opcodes, strings, integers, bools)
            # Ignore ENDDEF
            counter += 1
    return ProgramBox(functions)
