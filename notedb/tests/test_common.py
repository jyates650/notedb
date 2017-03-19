import os

from nose.tools import raises, eq_
from tests import test_files_dir
from notedb.common import (get_dataframe_from_csv, get_dataframe_from_xls,
    NotedbUserError)


class TestCommon:
    
    def test_read_csv(self):
        csv_file = os.path.join(test_files_dir, 'tape_headers.csv')
        my_df = get_dataframe_from_csv(csv_file)
        eq_(my_df.columns.tolist(), ['Aaa', 'Bbb', 'Ccc', 'Ddd', 'Eee'])
        eq_(my_df.iloc[0].tolist(), ['A', 'B', 'C', 'D', ''])    
    
    @raises(NotedbUserError)
    def test_read_csv_no_file(self):
        get_dataframe_from_csv('bogus_file')
    
    @raises(NotedbUserError)
    def test_read_csv_bad_format(self):
        not_csv_file = os.path.join(test_files_dir, 'test_tape.xlsx')
        get_dataframe_from_csv(not_csv_file)
    
    def test_read_excel(self):
        xls_file = os.path.join(test_files_dir, 'test_tape.xlsx')
        my_df = get_dataframe_from_xls(xls_file)
        eq_(my_df.columns.tolist(), ['aa', 'bb', 'E', 'dd'])
        eq_(my_df.iloc[1].tolist(), [43.5, 'FkdV', 4356, 'Beth Yarn'])
 
    @raises(NotedbUserError)
    def test_read_xls_no_file(self):
        get_dataframe_from_xls('bogus_file')
    
    @raises(NotedbUserError)
    def test_read_xls_bad_format(self):
        not_xls_file = os.path.join(test_files_dir, 'not_excel_file.txt')
        get_dataframe_from_xls(not_xls_file)