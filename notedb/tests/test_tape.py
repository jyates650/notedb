import os
import shutil
from notedb.tape import TapeParser

class TestTapeParser:

    def setUp(self):
        self.config = {'column_mapping': {'Header1': 'TestHeader1', 'Header2': 'TestHeader2'}}
        tests_dir = os.path.dirname(os.path.abspath(__file__))
        self.temp_dir = os.path.join(tests_dir, 'temp')
        os.mkdir(self.temp_dir)
        test_files_dir = os.path.join(tests_dir, 'test_files') 
        self.simple_test_tape_xlsx = os.path.join(test_files_dir, 'simple_test_tape.xlsx')
        self.tape_headers_csv = os.path.join(test_files_dir, 'tape_headers.csv')
        self.test_tape_format_1_xlsx = os.path.join(test_files_dir, 'test_tape_format_1.xlsx')
        
    def tearDown(self):
        shutil.rmtree(self.temp_dir)
        
    def test_excel_parsing(self):
        tape_parser = TapeParser(self.simple_test_tape_xlsx)
        df = tape_parser.tape_df
        assert df['TestHeader1'][0] == 'TestData11'
        assert df['TestHeader1'][1] == 'TestData21'
        assert df['TestHeader2'][0] == 'TestData12'
        assert df['TestHeader2'][1] == 'TestData22'
        
    def test_pandas_rename_column(self):
        tape_parser = TapeParser(self.simple_test_tape_xlsx)
        df = tape_parser.tape_df
        df.rename(columns={'TestHeader1': 'Header1'}, inplace=True)
        assert df['Header1'][0] == 'TestData11'
    
    def test_format_tape_columns(self):
        tape_parser = TapeParser(self.test_tape_format_1_xlsx)
        df = tape_parser.tape_df
        assert df['City'][0] == 'Methuen'
        assert len(df.columns) == 5
        assert df.columns.tolist() == ['State', 'Address', 'City', 'Zip', 'BPO']
        tape_parser.format_tape_columns(self.tape_headers_csv, 'format1')
        assert df['PropCity'][1] == 'Carlisle'
        assert df['Comment'][0] == ''
        assert len(df.columns) == 6
        
    def test_reorder_tape_columns(self):
        tape_parser = TapeParser(self.simple_test_tape_xlsx)
        df = tape_parser.tape_df
        df_cols = df.columns.tolist()
        assert df_cols == ['TestHeader1', 'TestHeader2']
        new_order = ['TestHeader2', 'TestHeader1']
        tape_parser._reorder_columns(new_order)
        assert tape_parser.tape_df.columns.tolist() == new_order
        
    def test_excel_writing(self):
        tape_parser = TapeParser(self.simple_test_tape_xlsx)
        df1 = tape_parser.tape_df
        out_file = os.path.join(self.temp_dir, 'outfile1.xlsx')
        tape_parser.write_tape_xls(out_file)
        tp2 = TapeParser(out_file)
        df2 = tp2.tape_df
        assert df1['TestHeader1'][1] == df2['TestHeader1'][1]
        
    def test_rename_and_reorder_tape_cols(self):
        tape_parser = TapeParser(self.test_tape_format_1_xlsx)
        cols = tape_parser.tape_df.columns.tolist()
        assert cols == ['State', 'Address', 'City', 'Zip', 'BPO']
        tape_parser.format_tape_columns(self.tape_headers_csv, 'format1')
        cols = tape_parser.tape_df.columns.tolist()
        assert cols == ['PropAddr', 'PropCity', 'PropState', 'PropZip', 'BPO', 'Comment']
        