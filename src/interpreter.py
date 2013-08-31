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

# Set this switch to True to run this interpreter with CPython
# Set this switch to False to compile this interpreter with rpython
DEBUG = False

import os
import sys

from box import IntBox
from box import StringBox
from box import BoolBox

if not DEBUG:
    from rpython.rlib import rstring

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
    }


def parse_bytecode_file(bytecode_file):
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


def mainloop(bytecode, strings, integers, bools):
    pc = 0
    heap = {} # Only have a global heap for now.
    stack = []
    while pc < len(bytecode):
        # Arithmetic operation bytecodes.
        if bytecode[pc] == OPCODES['ADD']:
            l = stack.pop()
            r = stack.pop()
            stack.append(l.add(r))
        elif bytecode[pc] == OPCODES['MINUS']:
            l = stack.pop()
            r = stack.pop()
            stack.append(l.minus(r))
        elif bytecode[pc] == OPCODES['TIMES']:
            l = stack.pop()
            r = stack.pop()
            stack.append(l.times(r))
        elif bytecode[pc] == OPCODES['DIV']:
            l = stack.pop()
            r = stack.pop()
            stack.append(l.div(r))
        elif bytecode[pc] == OPCODES['MOD']:
            l = stack.pop()
            r = stack.pop()
            stack.append(l.mod(r))
        # Comparative operation bytecodes.
        elif bytecode[pc] == OPCODES['GT']:
            l = stack.pop()
            r = stack.pop()
            stack.append(l.gt(r))
        elif bytecode[pc] == OPCODES['LT']:
            l = stack.pop()
            r = stack.pop()
            stack.append(l.lt(r))
        elif bytecode[pc] == OPCODES['GEQ']:
            l = stack.pop()
            r = stack.pop()
            stack.append(l.geq(r))
        elif bytecode[pc] == OPCODES['LEQ']:
            l = stack.pop()
            r = stack.pop()
            stack.append(l.leq(r))
        elif bytecode[pc] == OPCODES['EQ']:
            l = stack.pop()
            r = stack.pop()
            stack.append(l.eq(r))
        elif bytecode[pc] == OPCODES['NEQ']:
            l = stack.pop()
            r = stack.pop()
            stack.append(l.neq(r))        
        # I/O bytecodes.
        elif bytecode[pc] == OPCODES['PRINT_ITEM']:
            value = stack.pop()
            value.print_nl()
        elif bytecode[pc] == OPCODES['PRINT_NEWLINE']:
            print
        # Global variable bytecodes.
        elif bytecode[pc] == OPCODES['STORE']:
            # TODO: A bit of error checking here would be nice.
            name = stack.pop().string
            lit = stack.pop().integer
            heap[name] =  lit
        elif bytecode[pc] == OPCODES['LOAD_GLOBAL']:
            # TODO: Should the heap really hold raw string / int types?
            # TODO: Probably not.
            g = heap[strings[bytecode[pc + 1]]]
            stack.append(IntBox(g))
            pc += 1
        elif bytecode[pc] == OPCODES['LOAD_CONST']:
            const = integers[bytecode[pc + 1]]
            stack.append(IntBox(const))
            pc += 1
        elif bytecode[pc] == OPCODES['LOAD_NAME']:
            name = strings[bytecode[pc + 1]]
            stack.append(StringBox(name))
            pc += 1
        pc += 1
    return


def run(fp):
    program_contents = ""
    while True:
        read = os.read(fp, 4096)
        if len(read) == 0:
            break
        program_contents += read
    os.close(fp)
    bytecode, strings, integers, bools = parse_bytecode_file(program_contents)
    mainloop(bytecode, strings, integers, bools)


def entry_point(argv):
    try:
        filename = argv[1]
    except IndexError:
        print "You must supply a filename"
        return 1
    run(os.open(filename, os.O_RDONLY, 0777))
    return 0


def target(*args):
    return entry_point, None


if __name__ == "__main__":
    entry_point(sys.argv)
