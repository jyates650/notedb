import os
from notedb.tape import TapeParser

class TestTapeParser:

    def setUp(self):
        self.config = {'column_mapping': {'Header1': 'TestHeader1', 'Header2': 'TestHeader2'}}
        tests_dir = os.path.dirname(os.path.abspath(__file__))
        test_files_dir = os.path.join(tests_dir, 'test_files') 
        self.simple_test_tape_xlsx = os.path.join(test_files_dir, 'simple_test_tape.xlsx')
        
    def test_excel_parsing(self):
        tape_parser = TapeParser(self.config)
        tape_parser.parse_new_tape_xls(self.simple_test_tape_xlsx)
        df = tape_parser.data_frame
        assert df['TestHeader1'][0] == 'TestData11'
        assert df['TestHeader1'][1] == 'TestData21'
        assert df['TestHeader2'][0] == 'TestData12'
        assert df['TestHeader2'][1] == 'TestData22'
        
    def test_pandas_rename_column(self):
        tape_parser = TapeParser(self.config)
        tape_parser.parse_new_tape_xls(self.simple_test_tape_xlsx)
        df = tape_parser.data_frame
        df.rename(columns={'TestHeader1': 'Header1'}, inplace=True)
        assert df['Header1'][0] == 'TestData11'
        
        
    def test_standardize_column_names(self):
        tape_parser = TapeParser(self.config)
        tape_parser.parse_new_tape_xls(self.simple_test_tape_xlsx)
        tape_parser.standardize_column_names()
        df = tape_parser.data_frame
        assert df['Header1'][0] == 'TestData11'
        assert df['Header1'][1] == 'TestData21'
        assert df['Header2'][0] == 'TestData12'
        assert df['Header2'][1] == 'TestData22'