
import pandas
import numpy

from notedb.tape import TapeFormatter
from pandas.util.testing import assert_series_equal
from nose.tools import eq_, raises
from notedb.common import NotedbUserError

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