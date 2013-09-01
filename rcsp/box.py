"""
Interpreter for a simple CSP language.

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

# pylint: disable=W0613
# pylint: disable=W0231

from rcsp.parser import opcode

# Set this switch to True to run this interpreter with CPython
# Set this switch to False to compile this interpreter with rpython
DEBUG = True


__date__ = 'August 2013'
__author__ = 'Sarah Mount <s.mount@wlv.ac.uk>'


class Box:

    def __init__(self):
        raise NotImplementedError

    def value(self):
        return self.value

class IntBox(Box):
    # TODO: Some of these could be collapsed and refactored.
    
    def __init__(self, integer):
        self.integer = integer

    def add(self, integer):
        if isinstance(integer, IntBox):
            return IntBox(self.integer + integer.integer)
        raise TypeError("Was expecting an IntBox")
        
    def minus(self, integer):
        if isinstance(integer, IntBox):
            return IntBox(self.integer - integer.integer)
        raise TypeError
        
    def times(self, integer):
        if isinstance(integer, IntBox):
            return IntBox(self.integer * integer.integer)
        raise TypeError
        
    def div(self, integer):
        if isinstance(integer, IntBox):
            return IntBox(self.integer / integer.integer)
        raise TypeError
        
    def mod(self, integer):
        if isinstance(integer, IntBox):
            return IntBox(self.integer % integer.integer)
        raise TypeError

    def gt(self, integer):
        if isinstance(integer, IntBox):
            if self.integer > integer.integer:
                return BoolBox(True)
            else: return BoolBox(False)
        raise TypeError

    def lt(self, integer):
        if isinstance(integer, IntBox):
            if self.integer < integer.integer:
                return BoolBox(True)
            else: return BoolBox(False)
        raise TypeError

    def geq(self, integer):
        if isinstance(integer, IntBox):
            if self.integer >= integer.integer:
                return BoolBox(True)
            else: return BoolBox(False)
        raise TypeError

    def leq(self, integer):
        if isinstance(integer, IntBox):
            if self.integer <= integer.integer:
                return BoolBox(True)
            else: return BoolBox(False)
        raise TypeError

    def eq(self, integer):
        if isinstance(integer, IntBox):
            if self.integer == integer.integer:
                return BoolBox(True)
            else: return BoolBox(False)
        raise TypeError

    def neq(self, integer):
        if isinstance(integer, IntBox):
            if self.integer != integer.integer:
                return BoolBox(True)
            else: return BoolBox(False)
        raise TypeError

    def __repr__(self):
        return str(self.integer)

    def __str__(self):
        return str(self.integer)

    def __eq__(self, other):
        if isinstance(other, IntBox):
            if self.integer == other.integer:
                return True
        return False

    
class StringBox(Box):

    def __init__(self, string):
        self.string = string

    def print_nl(self):
        print self.string

    def __repr__(self):
        return self.string

    def __str__(self):
        return self.string

    def __eq__(self, other):
        if isinstance(other, StringBox):
            if self.string == other.string:
                return True
        return False


class BoolBox(Box):

    def __init__(self, boolean):
        self.boolean = boolean

    def print_nl(self):
        print self.boolean

    def __repr__(self):
        return str(self.boolean)

    def __str__(self):
        return str(self.boolean)

    def __eq__(self, other):
        if isinstance(other, BoolBox):
            if self.boolean == other.boolean:
                return True
        return False


class CodeBox(Box):
    
    def __init__(self, bytecode, strings, integers, bools):
        self.bytecode = bytecode
        self.strings = strings
        self.integers = integers
        self.bools = bools

    def __repr__(self):
        """Pretty print a list of numeric opcodes and lists of constants.
        This is intended to pretty-print the output of the parser.
        """
        def new_bc(bc, pc, output):
            output.append(str(pc) + ':\t' + bc)
        pc = 0
        output = ['CODE']
        while pc < len(self.bytecode):
            # Arithmetic operation bytecodes.
            if self.bytecode[pc] == opcode('ADD'):
                new_bc('ADD', pc, output)
            elif self.bytecode[pc] == opcode('MINUS'):
                new_bc('MINUS', pc, output)
            elif self.bytecode[pc] == opcode('TIMES'):
                new_bc('TIMES', pc, output)
            elif self.bytecode[pc] == opcode('DIV'):
                new_bc('DIV', pc, output)
            elif self.bytecode[pc] == opcode('MOD'):
                new_bc('MOD', pc, output)
            # Comparative operation bytecodes.
            elif self.bytecode[pc] == opcode('GT'):
                new_bc('GT', pc, output)
            elif self.bytecode[pc] == opcode('LT'):
                new_bc('LT', pc, output)
            elif self.bytecode[pc] == opcode('GEQ'):
                new_bc('GEQ', pc, output)
            elif self.bytecode[pc] == opcode('LEQ'):
                new_bc('LEQ', pc, output)
            elif self.bytecode[pc] == opcode('EQ'):
                new_bc('EQ', pc, output)
            elif self.bytecode[pc] == opcode('NEQ'):
                new_bc('NEQ', pc, output)
            # I/O bytecodes.
            elif self.bytecode[pc] == opcode('PRINT_ITEM'):
                new_bc('PRINT_ITEM', pc, output)
            elif self.bytecode[pc] == opcode('PRINT_NEWLINE'):
                new_bc('PRINT_NEWLINE', pc, output)
            # Global variable bytecodes.
            elif self.bytecode[pc] == opcode('STORE'):
                new_bc('STORE', pc, output)
            elif self.bytecode[pc] == opcode('LOAD_GLOBAL'):
                new_bc('LOAD_GLOBAL ' +
                       str(self.bytecode[pc + 1]) + '\t(' +
                       self.strings[self.bytecode[pc + 1]] + ')', 
                       pc,
                       output)
                pc += 1
            elif self.bytecode[pc] == opcode('LOAD_CONST'):
                new_bc('LOAD_CONST ' +
                       str(self.bytecode[pc + 1]) + '\t(' +
                       str(self.integers[self.bytecode[pc + 1]]) + ')',
                       pc,
                       output)
                pc += 1
            elif self.bytecode[pc] == opcode('LOAD_NAME'):
                new_bc('LOAD_NAME ' +
                       str(self.bytecode[pc + 1]) + '\t(' +
                       self.strings[self.bytecode[pc + 1]] + ')',
                       pc,
                       output)
                pc += 1
            # Control flow.
            elif self.bytecode[pc] == opcode('JUMP_FORWARD'):
                new_bc('JUMP_FORWARD ' +
                       str(self.bytecode[pc + 1]) + '\t(' +
                       str(self.integers[self.bytecode[pc + 1]]) + ')',
                       pc,
                       output)
                pc = pc + 1
            elif self.bytecode[pc] == opcode('POP_JUMP_IF_TRUE'):
                new_bc('POP_JUMP_IF_TRUE ' +
                       str(self.bytecode[pc + 1]) + '\t(' +
                       str(self.integers[self.bytecode[pc + 1]]) + ')',
                       pc,
                       output)
                pc += 1
            elif self.bytecode[pc] == opcode('POP_JUMP_IF_FALSE'):
                new_bc('POP_JUMP_IF_FALSE ' +
                       str(self.bytecode[pc + 1]) + '\t(' +
                       str(self.integers[self.bytecode[pc + 1]]) + ')',
                       pc,
                       output)
                pc += 1
            elif self.bytecode[pc] == opcode('JUMP_ABSOLUTE'):
                new_bc('POP_JUMP_IF_FALSE ' +
                       str(self.bytecode[pc + 1]) + '\t(' +
                       str(self.integers[self.bytecode[pc + 1]]) + ')',
                       pc,
                       output)
                pc += 1
            # Function creation and calls.
            elif self.bytecode[pc] == opcode('CALL_FUNCTION'):
                new_bc('CALL_FUNCTION ' +
                       str(self.bytecode[pc + 1]) + '\t(' +
                       str(self.strings[self.bytecode[pc + 1]]) + ')',
                       pc,
                       output)
                pc += 1
            elif self.bytecode[pc] == opcode('LOAD_ARG'):
                new_bc('LOAD_ARG ' +
                       str(self.bytecode[pc + 1]) + '\t(' +
                       str(self.strings[self.bytecode[pc + 1]]) + ')',
                       pc,
                       output)
                pc += 1
            elif self.bytecode[pc] == opcode('MAKE_FUNCTION'):
                new_bc('MAKE_FUNCTION', pc, output)
            elif self.bytecode[pc] == opcode('RETURN'):
                new_bc('RETURN ' +
                       str(self.bytecode[pc + 1]) + '\t(' +
                       str(self.integers[self.bytecode[pc + 1]]) + ')',
                       pc,
                       output)
                pc += 1
            # Unknown bytecode.
            else:
                raise TypeError('No such CSPC opcode')
            pc += 1
        output.append('\n')
        output.append('DATA:')
        output.append('\tIntegers: ' + repr(self.integers))
        output.append('\tStrings: ' + repr(self.strings))
        output.append('\tBools:' + repr(self.bools))
        output.append('\n')
        return '\n'.join(output)


class ProgramBox(Box):
    
    def __init__(self, cb_dict):
        self.functions = cb_dict # dict of code boxes

    def get(self, name):
        return self.functions[name]

    def get_functions(self):
        return self.functions.keys()

    def __repr__(self):
        output = ['\n', '...pretty printing parser output...']
        for name in self.functions:
            output.append('DEF ' + name + '\n')
            output.append(repr(self.functions[name]))
            output.append('ENDDEF')
        output.append('...pretty printer done...')
        output.append('\n')
        return '\n'.join(output)
