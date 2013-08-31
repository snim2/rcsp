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

try:
    from rpython.rlib import rstring
except ImportError:
    pass


__date__ = 'August 2013'
__author__ = 'Sarah Mount <s.mount@wlv.ac.uk>'


OPCODES = {
    # Integer arithmetic.
    'ADD' : 0, 'MINUS' : 1, 'TIMES' : 2, 'DIV' : 3, 'MOD' : 4,
    # Integer comparisons.
    'GT' : 5, 'LT': 6, 'EQ' : 7, 'NEQ' : 8, 'GEQ' : 9, 'LEQ' : 10,
    # I/O.
    'PRINT_ITEM' : 11, 'PRINT_NEWLINE' : 12,
    # Global variables.
    'STORE' : 13, 'LOAD_GLOBAL' : 14, 'LOAD_CONST' : 15, 'LOAD_NAME' : 16,
    # Control flow.
    'JUMP_FORWARD' : 17, 'POP_JUMP_IF_TRUE' : 18, 'POP_JUMP_IF_FALSE' : 19,
    'JUMP_ABSOLUTE' : 20,
    }


def pretty_print(bytecode, strings, integers, bools):
    """Pretty print a list of numeric opcodes and lists of constants.
    This is intended to pretty-print the output of the parser.
    """
    def new_bc(bc, pc, output):
        output.append(str(pc) + ':\t' + bc)
    pc = 0
    output = []
    while pc < len(bytecode):
        # Arithmetic operation bytecodes.
        if bytecode[pc] == OPCODES['ADD']:
            new_bc('ADD', pc, output)
        elif bytecode[pc] == OPCODES['MINUS']:
            new_bc('MINUS', pc, output)
        elif bytecode[pc] == OPCODES['TIMES']:
            new_bc('TIMES', pc, output)
        elif bytecode[pc] == OPCODES['DIV']:
            new_bc('DIV', pc, output)
        elif bytecode[pc] == OPCODES['MOD']:
            new_bc('MOD', pc, output)
        # Comparative operation bytecodes.
        elif bytecode[pc] == OPCODES['GT']:
            new_bc('GT', pc, output)
        elif bytecode[pc] == OPCODES['LT']:
            new_bc('LT', pc, output)
        elif bytecode[pc] == OPCODES['GEQ']:
            new_bc('GEQ', pc, output)
        elif bytecode[pc] == OPCODES['LEQ']:
            new_bc('LEQ', pc, output)
        elif bytecode[pc] == OPCODES['EQ']:
            new_bc('EQ', pc, output)
        elif bytecode[pc] == OPCODES['NEQ']:
            new_bc('NEQ', pc, output)
        # I/O bytecodes.
        elif bytecode[pc] == OPCODES['PRINT_ITEM']:
            new_bc('PRINT_ITEM', pc, output)
        elif bytecode[pc] == OPCODES['PRINT_NEWLINE']:
            new_bc('PRINT_NEWLINE', pc, output)
        # Global variable bytecodes.
        elif bytecode[pc] == OPCODES['STORE']:
            new_bc('STORE', pc, output)
        elif bytecode[pc] == OPCODES['LOAD_GLOBAL']:
            new_bc('LOAD_GLOBAL ' + strings[bytecode[pc + 1]],
                   pc,
                   output)
            pc += 1
        elif bytecode[pc] == OPCODES['LOAD_CONST']:
            new_bc('LOAD_CONST ' + str(integers[bytecode[pc + 1]]),
                   pc,
                   output)
            pc += 1
        elif bytecode[pc] == OPCODES['LOAD_NAME']:
            new_bc('LOAD_NAME ' + strings[bytecode[pc + 1]],
                   pc,
                   output)
            pc += 1
        # Control flow.
        elif bytecode[pc] == OPCODES['JUMP_FORWARD']:
            new_bc('JUMP_FORWARD ' + str(integers[bytecode[pc + 1]]),
                   pc,
                   output)
            pc = pc + 1
        elif bytecode[pc] == OPCODES['POP_JUMP_IF_TRUE']:
            new_bc('POP_JUMP_IF_TRUE ' + str(integers[bytecode[pc + 1]]),
                   pc,
                   output)
            pc += 1
        elif bytecode[pc] == OPCODES['POP_JUMP_IF_FALSE']:
            new_bc('POP_JUMP_IF_FALSE ' + str(integers[bytecode[pc + 1]]),
                   pc,
                   output)
            pc += 1
        elif bytecode[pc] == OPCODES['JUMP_ABSOLUTE']:
            new_bc('POP_JUMP_IF_FALSE ' + str(integers[bytecode[pc + 1]]),
                   pc,
                   output)
            pc += 1
        else:
            raise TypeError('No such CSPC opcode')
        pc += 1
    print 
    print '...pretty printing parser output...'
    print
    print '\n'.join(output)
    print
    print 'Integers:', integers
    print 'Strings:', strings
    print 'Bools:', bools
    print
    print '...pretty printer done...'
    print
    return    


def parse_bytecode_file(bytecode_file, DEBUG=False):
    """Parse a file of bytecode.

    The argument should be the text of the original file, with
    mnemonic bytecodes. The result will be a list of numeric opcodes,
    defined by the OPCODES dictionary above, and lists of constants,
    in this order:

        opcodes, strings, integers, bools
    """
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
    opcodes, strings, integers, bools = [], [], [], []
    for code in bytecode:
        # Handle instructions.
        if code in OPCODES.keys():
            opcodes.append(OPCODES[code])
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
    return opcodes, strings, integers, bools
