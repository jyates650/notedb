import os
import pandas

from nose.tools import raises
from notedb.common import NotedbUserError
from notedb.tape import Tape
from pandas.util.testing import assert_frame_equal
from tests import test_files_dir


class TestTape:
    
    test_df = pandas.DataFrame([[23.4, 'asdf', 189, 'Nod Gool'],
                                [43.5, 'FkdV', 4356, 'Beth Yarn'],
                                [90.9, 'RegF', 239, 'Fan Yung']],
                               columns = ['aa', 'bb', 'E', 'dd'])
                
    def test_read_xls(self):
        my_tape = Tape()
        input_xls = os.path.join(test_files_dir, 'test_tape.xlsx')
        my_tape.read_xls(input_xls)
        assert_frame_equal(self.test_df, my_tape.dataframe)   
    
    @raises(NotedbUserError)
    def test_read_xls_file_not_found(self):
        my_tape = Tape()
        my_tape.read_xls('bogus_tape_file')
        
    @raises(NotedbUserError)
    def test_read_xls_wrong_format(self):
        my_tape = Tape()
        non_excel_file = os.path.join(test_files_dir, 'not_excel_file.txt')
        my_tape.read_xls(non_excel_file)