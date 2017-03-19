import os
import pandas
import numpy

from notedb.tape import TapeFormatter
from pandas.util.testing import assert_series_equal
from nose.tools import eq_, raises
from notedb.common import NotedbUserError
from tests import test_files_dir

class TestTapeFormatter:
    
    test_df = pandas.DataFrame(numpy.random.randn(6,4), columns=list('ABCD'))
    
    def setup(self):
        """This runs before every TestTapeFormatter test method"""
        new_df = self.test_df.copy()
        self.formatter = TapeFormatter(new_df)
    
    def test_rename_column(self):
        assert_series_equal(self.formatter.dataframe['B'], self.test_df['B'])
        self.formatter.rename_column(old_name='B', new_name='Boy')
        eq_(self.formatter.dataframe.columns.tolist(), ['A', 'Boy', 'C', 'D'])
        eq_(self.formatter.dataframe['Boy'].tolist(), self.test_df['B'].tolist())
        
    @raises(KeyError)
    def test_rename_column_doesnt_exist(self):
        self.formatter.rename_column(old_name='Bogus', new_name='Super_Bogus')
        
    @raises(NotedbUserError)
    def test_create_column_already_exists(self):
        self.formatter.create_column('B', 'bogus_value')
        
    def test_create_column_with_single_value(self):
        self.formatter.create_column('my_col', 'my_value')
        new_col = self.formatter.dataframe['my_col'].tolist()
        eq_(new_col, ['my_value']*6)
        
    def test_create_column_with_no_value(self):
        self.formatter.create_column('foo')
        new_col = self.formatter.dataframe['foo'].tolist()
        eq_(new_col, [None]*6)
        
    def test_create_column_with_values_list(self):      
        my_vals = [1, 3, 5, 7, 9, 11]
        self.formatter.create_column('bar', my_vals)
        new_col = self.formatter.dataframe['bar'].tolist()
        eq_(new_col, my_vals)
        
    def test_format_columns_from_full_map(self):
        format_map = {'Aaa': 'A', 'Bbb': 'B', 'Ccc': 'C', 'Ddd': 'D', 'Eee': 'E'}
        self.formatter.format_columns_from_map(format_map)
        new_cols = ['Aaa', 'Bbb', 'Ccc', 'Ddd', 'Eee']
        eq_(new_cols, self.formatter.dataframe.columns.tolist())
        new_col_eee = self.formatter.dataframe['Eee'].tolist()
        eq_(new_col_eee, [None]*6)
        
    def test_format_columns_from_partial_map(self):
        format_map = {'Bbb': 'B', 'Foo': None}
        self.formatter.format_columns_from_map(format_map)
        new_cols = ['A', 'Bbb', 'C', 'D', 'Foo']
        eq_(new_cols, self.formatter.dataframe.columns.tolist())
        new_col_foo = self.formatter.dataframe['Foo'].tolist()
        eq_(new_col_foo, [None]*6)
        
    def test_format_columns_from_csv(self):
        format_csv = os.path.join(test_files_dir, 'tape_headers.csv')
        self.formatter.format_columns_from_csv(format_csv)
        new_cols = ['Aaa', 'Bbb', 'Ccc', 'Ddd', 'Eee']
        eq_(new_cols, self.formatter.dataframe.columns.tolist())
        new_col_eee = self.formatter.dataframe['Eee'].tolist()
        eq_(new_col_eee, [None]*6)
