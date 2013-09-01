"""
Test the interpreter on all example files in the tests/
directory. Each file should contain bytecode and a commented section
like this:

# TEST_DATA
# expected = ...
# expected_stack = ...
# expected_heap = ...
# END_TEST_DATA

which state the expected output of the parser and interpreter to test
against.

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

import sys
sys.path.insert(0, "..")

# pylint: disable=W0122

# from __future__ import absolute_import # FIXME - this would be better.

import pytest
from glob import glob
from rcsp.parser import parse_bytecode_file

from rcsp.parser import OPCODES          # Needed by exec()
from rcsp.box import ProgramBox, CodeBox # Needed by exec()


def assert_programs_equal(actual, expected):
    """Test whether two ProgramBox objects are the same.
    """
    for fn in expected.get_functions():
        assert actual.get(fn) is not None
        assert expected.get(fn).bytecode == actual.get(fn).bytecode
        assert expected.get(fn).strings == actual.get(fn).strings
        assert expected.get(fn).integers == actual.get(fn).integers
        assert expected.get(fn).bools == actual.get(fn).bools
    return


def get_expected_results(code):
    """Given text from a test file, find the expected output of the parser.

    This should be stored in the (commented) TEST_DATA section of the
    test file.
    """
    py_code = []
    bytecode = code.split('\n')
    for lineno, line in enumerate(bytecode):
        if (line.strip().startswith('# ') and
            len(line.strip()) > 8):
            if bytecode[lineno][2:] != 'TEST_DATA':
                continue
            else:
                lineno +=1
                while len(bytecode[lineno]) < 3:
                    lineno += 1 
            while bytecode[lineno][2:] != 'END_TEST_DATA':
                py_code.append(bytecode[lineno][2:])
                lineno += 1
                while len(bytecode[lineno]) < 3:
                    lineno += 1 
    test_data = '\n'.join(py_code)
    exec(test_data)
    # Return variables defined in the eval
    return expected, expected_stack, expected_heap


def process_one_file(filename):
    """Process one test file.

    Parse the file, get the expected parser output from the test file
    and assert that the actual and expected results of the parser are
    identical.
    """
    with open(filename) as fn:
        bytecode = fn.read()
    actual = parse_bytecode_file(bytecode)
    expected, _, _ = get_expected_results(bytecode)
    assert_programs_equal(actual, expected)
    return


@pytest.mark.parametrize(("filename",),
                         [(foo,) for foo in glob('tests/example*.cspc')]) 
def test_all_files(filename):
    """Test all example files in the tests/ directory.
    """
    process_one_file(filename)
    return

