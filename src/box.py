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
