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

import os
import sys


__date__ = 'August 2013'
__author__ = 'Sarah Mount <s.mount@wlv.ac.uk>'


def parse_bytecode_file(bytecode_file):
    bytecode = []
    for line_ in bytecode_file.split('\n'):
        line = line_.strip()
        if line.startswith('#'):
            continue
        else:
            for code in line.split(): bytecode.append(code)
    return bytecode


def mainloop(bytecode):
    pc = 0
    heap = dict() # Only have a global heap for now.
    stack = []
    while pc < len(bytecode):
        if bytecode[pc] == 'ADD':
            l = stack.pop()
            r = stack.pop()
            stack.append(l + r)
        elif bytecode[pc] == 'MINUS':
            l = stack.pop()
            r = stack.pop()
            stack.append(l - r)
        elif bytecode[pc] == 'TIMES':
            l = stack.pop()
            r = stack.pop()
            stack.append(l * r)
        elif bytecode[pc] == 'DIV':
            l = stack.pop()
            r = stack.pop()
            stack.append(l / r)
        elif bytecode[pc] == 'MOD':
            l = stack.pop()
            r = stack.pop()
            stack.append(l % r)
        elif bytecode[pc] == 'PRINT_ITEM':
            print stack.pop(),
        elif bytecode[pc] == 'PRINT_NEWLINE':
            print 
        elif bytecode[pc] == 'STORE':
            name = stack.pop()
            lit = stack.pop()
            heap[name] =  lit
        elif bytecode[pc] == 'LOAD_GLOBAL':
            g = heap[bytecode[pc + 1]]
            stack.append(g)
            pc += 1
        elif bytecode[pc] == 'LOAD_CONST':
            const = int(bytecode[pc + 1])
            stack.append(const)
            pc += 1
        elif bytecode[pc] == 'LOAD_NAME':
            name = bytecode[pc + 1]
            stack.append(name)
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
    bytecode = parse_bytecode_file(program_contents)
    mainloop(bytecode)


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
