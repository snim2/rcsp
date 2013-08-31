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

from parser import OPCODES

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

    def print_nl(self):
        print self.integer


class StringBox(Box):

    def __init__(self, string):
        self.string = string

    def print_nl(self):
        print self.string


class BoolBox(Box):

    def __init__(self, boolean):
        self.boolean = boolean

    def print_nl(self):
        print self.boolean


class CodeBox(Box):
    
    def __init__(self, bytecode, strings, integers, bools, codes):
        self.bytecode = bytecode
        self.strings = strings
        self.integers = integers
        self.bools = bools
        self.codes = codes

    def pretty_print(self):
        """Pretty print a list of numeric opcodes and lists of constants.
        This is intended to pretty-print the output of the parser.
        """
        def new_bc(bc, pc, output):
            output.append(str(pc) + ':\t' + bc)
        pc = 0
        output = []
        while pc < len(self.bytecode):
            # Arithmetic operation bytecodes.
            if self.bytecode[pc] == OPCODES['ADD']:
                new_bc('ADD', pc, output)
            elif self.bytecode[pc] == OPCODES['MINUS']:
                new_bc('MINUS', pc, output)
            elif self.bytecode[pc] == OPCODES['TIMES']:
                new_bc('TIMES', pc, output)
            elif self.bytecode[pc] == OPCODES['DIV']:
                new_bc('DIV', pc, output)
            elif self.bytecode[pc] == OPCODES['MOD']:
                new_bc('MOD', pc, output)
            # Comparative operation bytecodes.
            elif self.bytecode[pc] == OPCODES['GT']:
                new_bc('GT', pc, output)
            elif self.bytecode[pc] == OPCODES['LT']:
                new_bc('LT', pc, output)
            elif self.bytecode[pc] == OPCODES['GEQ']:
                new_bc('GEQ', pc, output)
            elif self.bytecode[pc] == OPCODES['LEQ']:
                new_bc('LEQ', pc, output)
            elif self.bytecode[pc] == OPCODES['EQ']:
                new_bc('EQ', pc, output)
            elif self.bytecode[pc] == OPCODES['NEQ']:
                new_bc('NEQ', pc, output)
            # I/O bytecodes.
            elif self.bytecode[pc] == OPCODES['PRINT_ITEM']:
                new_bc('PRINT_ITEM', pc, output)
            elif self.bytecode[pc] == OPCODES['PRINT_NEWLINE']:
                new_bc('PRINT_NEWLINE', pc, output)
            # Global variable bytecodes.
            elif self.bytecode[pc] == OPCODES['STORE']:
                new_bc('STORE', pc, output)
            elif self.bytecode[pc] == OPCODES['LOAD_GLOBAL']:
                new_bc('LOAD_GLOBAL ' + self.strings[self.bytecode[pc + 1]],
                       pc,
                       output)
                pc += 1
            elif self.bytecode[pc] == OPCODES['LOAD_CONST']:
                new_bc('LOAD_CONST ' +
                       str(self.integers[self.bytecode[pc + 1]]),
                       pc,
                       output)
                pc += 1
            elif self.bytecode[pc] == OPCODES['LOAD_NAME']:
                new_bc('LOAD_NAME ' + self.strings[self.bytecode[pc + 1]],
                       pc,
                       output)
                pc += 1
            # Control flow.
            elif self.bytecode[pc] == OPCODES['JUMP_FORWARD']:
                new_bc('JUMP_FORWARD ' +
                       str(self.integers[self.bytecode[pc + 1]]),
                       pc,
                       output)
                pc = pc + 1
            elif self.bytecode[pc] == OPCODES['POP_JUMP_IF_TRUE']:
                new_bc('POP_JUMP_IF_TRUE ' +
                       str(self.integers[self.bytecode[pc + 1]]),
                       pc,
                       output)
                pc += 1
            elif self.bytecode[pc] == OPCODES['POP_JUMP_IF_FALSE']:
                new_bc('POP_JUMP_IF_FALSE ' +
                       str(self.integers[self.bytecode[pc + 1]]),
                       pc,
                       output)
                pc += 1
            elif self.bytecode[pc] == OPCODES['JUMP_ABSOLUTE']:
                new_bc('POP_JUMP_IF_FALSE ' +
                       str(self.integers[self.bytecode[pc + 1]]),
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
        print 'Integers:', self.integers
        print 'Strings:', self.strings
        print 'Bools:', self.bools
        print
        print '...pretty printer done...'
        print
        return    

