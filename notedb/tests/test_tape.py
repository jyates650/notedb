"""Unit tests for the Tape module"""

import os
import pandas

from nose.tools import raises, eq_
from notedb.common import NotedbUserError, get_dataframe_from_xls
from notedb.tape import Tape
from pandas.util.testing import assert_frame_equal
from tests import test_files_dir
from notedb.note import Address
import copy

class TestSimpleTape:
    """Class to test simple Tape operations"""

    test_df = pandas.DataFrame([[23.4, 'asdf', 189, 'Nod Gool'],
                                [43.5, 'FkdV', 4356, 'Beth Yarn'],
                                [90.9, 'RegF', 239, 'Fan Yung']],
                               columns = ['aa', 'bb', 'E', 'dd'])

    def test_read_xls(self):
        """Test that Tape can read a Tape xls"""
        my_tape = Tape()
        input_xls = os.path.join(test_files_dir, 'test_tape.xlsx')
        my_tape.read_xls(input_xls)
        assert_frame_equal(self.test_df, my_tape.dataframe)   

    @raises(NotedbUserError)
    def test_read_xls_file_not_found(self):
        """Test that file not found error raises Notedb exception"""
        my_tape = Tape()
        my_tape.read_xls('bogus_tape_file')

    @raises(NotedbUserError)
    def test_read_xls_wrong_format(self):
        """Test that wrong format of xls raises Notedb error"""
        my_tape = Tape()
        non_excel_file = os.path.join(test_files_dir, 'not_excel_file.txt')
        my_tape.read_xls(non_excel_file)


class TestRealTape:
    """Test Tape with real production column names"""
    
    tape = None
    
    @classmethod
    def setup_class(cls):
        """Create a Tape populated with some real looking data"""
        input_xls = os.path.join(test_files_dir, 'test_tape_format_1.xlsx')
        df = get_dataframe_from_xls(input_xls)
        cls.tape = Tape()
        cls.tape.dataframe = df

    def test_get_address(self):
        """Test that getting an Address from the note works"""
        note_data = self.tape.dataframe.iloc[0]
        addr = self.tape._get_address_object(note_data)
        eq_(str(addr), '8 Brown St, Methuen, MA 01844')

    def test_get_note(self):
        """Test getting a note from an Address and note data"""
        addr = Address('345 H St.', 'Sacramento', 'CA', 95811)
        note = self.tape._get_note_object(addr, 'bogus')
        eq_(note.address, addr)

    def test_pop_objects(self):
        """Test Tape can create Note objects containing address objects"""
        tape = copy.deepcopy(self.tape)
        tape.populate_database_objects()
        eq_(tape.notes[1].address.state, 'PA')
