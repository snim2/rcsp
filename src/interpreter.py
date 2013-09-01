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
# pylint: disable=W0602

import os
import sys

from box import IntBox
from box import StringBox
from box import BoolBox
from box import CodeBox

from parser import OPCODES, parse_bytecode_file, DEBUG

try:
    from rpython.rlib.jit import JitDriver
except ImportError:
    class JitDriver(object):
        def __init__(self,**kw): pass
        def jit_merge_point(self,**kw): pass
        def can_enter_jit(self,**kw): pass


# In the mainloop function green variables are read from, and
# red variables are written to.
jitdriver = JitDriver(greens=['pc', 'code'],
                      reds=['heap', 'stack'])

__date__ = 'August 2013'
__author__ = 'Sarah Mount <s.mount@wlv.ac.uk>'


def mainloop(program):
    """Main loop of the interpreter.
    """
    pc = 0
    heap = {} # Only have a global heap for now.
    stack = []
    code = program.get('main')
    while pc < len(code.bytecode):
        jitdriver.jit_merge_point(pc=pc, code=code, # Greens.
                                  # Reds:
                                  stack=stack, heap=heap)
        if DEBUG:
            print 'LEN:', len(code.bytecode), 'PC:', pc, '\tHEAP:', heap
        # Arithmetic operation code.bytecodes.
        if code.bytecode[pc] == OPCODES['ADD']:
            r = stack.pop()
            l = stack.pop()
            stack.append(l.add(r))
        elif code.bytecode[pc] == OPCODES['MINUS']:
            r = stack.pop()
            l = stack.pop()
            stack.append(l.minus(r))
        elif code.bytecode[pc] == OPCODES['TIMES']:
            r = stack.pop()
            l = stack.pop()
            stack.append(l.times(r))
        elif code.bytecode[pc] == OPCODES['DIV']:
            r = stack.pop()
            l = stack.pop()
            stack.append(l.div(r))
        elif code.bytecode[pc] == OPCODES['MOD']:
            r = stack.pop()
            l = stack.pop()
            stack.append(l.mod(r))
        # Comparative operation code.bytecodes.
        elif code.bytecode[pc] == OPCODES['GT']:
            r = stack.pop()
            l = stack.pop()
            stack.append(l.gt(r))
        elif code.bytecode[pc] == OPCODES['LT']:
            r = stack.pop()
            l = stack.pop()
            stack.append(l.lt(r))
        elif code.bytecode[pc] == OPCODES['GEQ']:
            r = stack.pop()
            l = stack.pop()
            stack.append(l.geq(r))
        elif code.bytecode[pc] == OPCODES['LEQ']:
            r = stack.pop()
            l = stack.pop()
            stack.append(l.leq(r))
        elif code.bytecode[pc] == OPCODES['EQ']:
            r = stack.pop()
            l = stack.pop()
            stack.append(l.eq(r))
        elif code.bytecode[pc] == OPCODES['NEQ']:
            r = stack.pop()
            l = stack.pop()
            stack.append(l.neq(r))        
        # I/O code.bytecodes.
        elif code.bytecode[pc] == OPCODES['PRINT_ITEM']:
            value = stack.pop()
            value.print_nl()
        elif code.bytecode[pc] == OPCODES['PRINT_NEWLINE']:
            print
        # Global variable code.bytecodes.
        elif code.bytecode[pc] == OPCODES['STORE']:
            # TODO: A bit of error checking here would be nice.
            name = stack.pop().string
            lit = stack.pop().integer
            heap[name] =  lit
        elif code.bytecode[pc] == OPCODES['LOAD_GLOBAL']:
            # TODO: Should the heap really hold raw string / int types?
            # TODO: Probably not.
            g = heap[code.strings[code.bytecode[pc + 1]]]
            stack.append(IntBox(g))
            pc += 1
        elif code.bytecode[pc] == OPCODES['LOAD_CONST']:
            const = code.integers[code.bytecode[pc + 1]]
            stack.append(IntBox(const))
            pc += 1
        elif code.bytecode[pc] == OPCODES['LOAD_NAME']:
            name = code.strings[code.bytecode[pc + 1]]
            stack.append(StringBox(name))
            pc += 1
        # Control flow.
        elif code.bytecode[pc] == OPCODES['JUMP_FORWARD']:
            delta = code.integers[code.bytecode[pc + 1]]
            pc += delta
        elif code.bytecode[pc] == OPCODES['POP_JUMP_IF_TRUE']:
            boolean = stack.pop()
            if boolean.boolean:
                new_pc = code.integers[code.bytecode[pc + 1]]
                pc = new_pc - 1
            else:
                pc += 1
        elif code.bytecode[pc] == OPCODES['POP_JUMP_IF_FALSE']:
            boolean = stack.pop()
            if not boolean.boolean:
                new_pc = code.integers[code.bytecode[pc + 1]]
                pc = new_pc - 1
            else:
                pc += 1
        elif code.bytecode[pc] == OPCODES['JUMP_ABSOLUTE']:
            new_pc = code.integers[code.bytecode[pc + 1]]
            pc = new_pc - 1
        # Function creation and calls.
        # TODO: 'CALL_FUNCTION'
        # TODO: 'LOAD_ARG'
        # TODO: 'MAKE_FUNCTION'
        # 'RETURN' : 24,
        elif code.bytecode[pc] == OPCODES['RETURN']:
            ret_value = code.integers[code.bytecode[pc + 1]]
            stack.append(ret_value)
            pc += 1
        # Unknown opcode.
        else:
            raise TypeError('No such CSPC opcode')
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
    program = parse_bytecode_file(program_contents)
    if DEBUG:
        program.pretty_print()
    mainloop(program)


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


def jitpolicy(driver):
    if not DEBUG:
        from rpython.jit.codewriter.policy import JitPolicy
        return JitPolicy()


if __name__ == "__main__":
    entry_point(sys.argv)
