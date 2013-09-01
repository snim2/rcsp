"""
Test the parser on all example files in the tests/ directory. Each
file should contain bytecode and a commented section like this:

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

# from __future__ import absolute_import # FIXME - this would be better.

from glob import glob
import pytest

from rcsp.parser import parse_bytecode_file
from rcsp.interpreter import mainloop

from tests.test_parser import get_expected_results


def assert_runtime_correct(actual_stack, actual_heap,
                           expected_stack, expected_heap):
    """Assert that expected and actual stack and heaps are identical.
    """
    assert actual_stack == expected_stack
    assert actual_heap == expected_heap
    return


def process_one_file(filename):
    """Process one test file.

    Parse and interpret the file, get the expected interpreter output
    from the test file and assert that the actual and expected results
    of the interpreter are identical.
    """
    with open(filename) as fn:
        bytecode = fn.read()
    prog_box = parse_bytecode_file(bytecode)
    actual_stack, actual_heap = mainloop(prog_box)
    _, expected_stack, expected_heap = get_expected_results(bytecode)
    assert_runtime_correct(actual_stack, actual_heap,
                           expected_stack, expected_heap)
    return


@pytest.mark.parametrize(("filename",),
                         [(foo,) for foo in glob('tests/example*.cspc')]) 
def test_all_files(filename):
    """Test all example files in the tests/ directory.
    """
    process_one_file(filename)
    return

