import pandas
import numpy

from notedb.tape import TapeFormatter
from pandas.util.testing import assert_series_equal
from nose.tools import eq_, raises

class TestTapeFormatter:
    
    test_df = pandas.DataFrame(numpy.random.randn(6,4), columns=list('ABCD'))
    
    def test_rename_column(self):
        new_df = self.test_df.copy()
        formatter = TapeFormatter(new_df)
        assert_series_equal(formatter.dataframe['B'], self.test_df['B'])
        formatter.rename_column(old_name='B', new_name='Boy')
        eq_(formatter.dataframe.columns.tolist(), ['A', 'Boy', 'C', 'D'])
        eq_(formatter.dataframe['Boy'].tolist(), self.test_df['B'].tolist())
        
    @raises(KeyError)
    def test_rename_column_doesnt_exist(self):
        new_df = self.test_df.copy()
        formatter = TapeFormatter(new_df)
        formatter.rename_column(old_name='Bogus', new_name='Super_Bogus')
        
    def test_create_column(self):
        pass