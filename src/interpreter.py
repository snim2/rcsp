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
            stack.append(stack.pop() + stack.pop())
        elif bytecode[pc] == 'MINUS':
            stack.append(stack.pop() - stack.pop())
        elif bytecode[pc] == 'TIMES':
            stack.append(stack.pop() * stack.pop())
        elif bytecode[pc] == 'DIV':
            stack.append(stack.pop() / stack.pop())
        elif bytecode[pc] == 'MOD':
            stack.append(stack.pop() % stack.pop())
        elif bytecode[pc] == 'PRINT_ITEM':
            print stack.pop(),
        elif bytecode[pc] == 'PRINT_NEWLINE':
            print 
        elif bytecode[pc] == 'STORE':
            heap[stack.pop()] =  stack.pop()
        elif bytecode[pc] == 'LOAD_GLOBAL':
            stack.append(heap[bytecode[pc + 1]])
            pc += 1
        elif bytecode[pc] == 'LOAD_CONST':
            stack.append(int(bytecode[pc + 1]))
            pc += 1
        elif bytecode[pc] == 'LOAD_NAME':
            stack.append(bytecode[pc + 1])
            pc += 1
        pc += 1
    return


def run(bytecode_file):
    mainloop(parse_bytecode_file(bytecode_file.read()))

    
if __name__ == "__main__":
    import sys
    run(open(sys.argv[1], 'r'))
