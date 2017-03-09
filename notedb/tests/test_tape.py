from notedb.tape import Tape

class TestTape:

    def setUp(self):
        self.config = {'column_mapping': {'Header1': 'TestHeader1', 'Header2': 'TestHeader2'}}
        
    def test_excel_parsing(self):
        new_tape = Tape(self.config)
        new_tape.parse_tape_excel_file('tests/test_files/simple_test_tape.xlsx')
        df = new_tape.data_frame
        assert df['TestHeader1'][0] == 'TestData11'
        assert df['TestHeader1'][1] == 'TestData21'
        assert df['TestHeader2'][0] == 'TestData12'
        assert df['TestHeader2'][1] == 'TestData22'
        
    def test_pandas_rename_column(self):
        new_tape = Tape(self.config)
        new_tape.parse_tape_excel_file('tests/test_files/simple_test_tape.xlsx')
        df = new_tape.data_frame
        df.rename(columns={'TestHeader1': 'Header1'}, inplace=True)
        assert df['Header1'][0] == 'TestData11'
        
        
    def test_standardize_column_names(self):
        new_tape = Tape(self.config)
        new_tape.parse_tape_excel_file('tests/test_files/simple_test_tape.xlsx')
        new_tape.standardize_column_names()
        df = new_tape.data_frame
        assert df['Header1'][0] == 'TestData11'
        assert df['Header1'][1] == 'TestData21'
        assert df['Header2'][0] == 'TestData12'
        assert df['Header2'][1] == 'TestData22'