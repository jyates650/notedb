import numpy
import os
import pandas
import shutil

from pandas.util.testing import assert_frame_equal
from notedb.common import NotedbUserError
from notedb.tape import TapeWriter
from nose.tools import raises
from openpyxl import load_workbook
from copy import deepcopy

class TestTapeWriter:
    
    tests_dir = os.path.dirname(os.path.abspath(__file__))
    temp_dir = os.path.join(tests_dir, 'temp')
    test_files_dir = os.path.join(tests_dir, 'test_files')
    test_df = pandas.DataFrame(numpy.random.randn(6,4), columns=list('ABCD'))
    template_xls = os.path.join(test_files_dir, 'test_template.xlsx')
    
    def setUp(self):
        os.mkdir(self.temp_dir)
        
    def tearDown(self):
        shutil.rmtree(self.temp_dir)
        
    def test_write_dataframe_to_xls(self):
        tape_writer = TapeWriter()
        output_xls = os.path.join(self.temp_dir, 'output1.xlsx')
        tape_writer.writer = pandas.ExcelWriter(output_xls, engine='openpyxl')
        tape_writer._write_dataframe_to_xls(self.test_df, output_xls)
        new_df = pandas.read_excel(output_xls)
        assert_frame_equal(self.test_df, new_df)
    
    def test_parse_template(self):
        tape_writer = TapeWriter()
        tape_writer.writer = pandas.ExcelWriter('bogus_file1', engine='openpyxl')
        template_df = pandas.DataFrame(columns=list('ABCDEF'))
        tape_writer._parse_template(self.template_xls)
        assert_frame_equal(tape_writer.template_df, template_df)
        assert 'Analysis' in tape_writer.writer.sheets
     
    @raises(NotedbUserError)   
    def test_parse_template_error(self):
        tape_writer = TapeWriter()
        tape_writer.writer = pandas.ExcelWriter('bogus_file2', engine='openpyxl')
        tape_writer._parse_template('bogus_file3')
    
    def test_write_xls_no_template(self):
        tape_writer = TapeWriter()
        output_xls = os.path.join(self.temp_dir, 'output2.xlsx')
        tape_writer.write_xls(self.test_df, output_xls)
        new_df = pandas.read_excel(output_xls)
        assert_frame_equal(self.test_df, new_df)
            
    def test_write_xls_with_template(self):
        tape_writer = TapeWriter()
        output_xls = os.path.join(self.temp_dir, 'output3.xlsx')
        tape_writer.write_xls(self.test_df, output_xls, self.template_xls)
        
        # Check that sheets were not destroyed by the write
        book = load_workbook(output_xls)
        assert list(ws.title for ws in book.worksheets) == ['Sheet1', 'Analysis']
        
        # Check that template data exists, with new columns
        new_df = pandas.read_excel(output_xls)
        assert new_df.columns.tolist() == list('ABCDEF')
        updated_df = self.test_df.copy()
        updated_df['E'] = numpy.NaN
        updated_df['F'] = numpy.NaN
        assert_frame_equal(updated_df, new_df)
        
        
        
        
        
        
        
