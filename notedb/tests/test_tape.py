from notedb.tape import Tape

class TestTape:
    
    def test_config_parsing(self):
        new_tape = Tape()
        new_tape.parse_tape_config_file('test_files/simple_test_tape.ini')
        col_map = new_tape.config['column_mapping']
        assert col_map['Header1'] == 'TestHeader1'
        assert col_map['Header2'] == 'TestHeader2'
        for key, value in new_tape.config['column_mapping'].items():
            assert col_map[key] == value
        
    def test_excel_parsing(self):
        new_tape = Tape()
        new_tape.parse_tape_excel_file('test_files/simple_test_tape.xlsx')
        df = new_tape.data_frame
        assert df['TestHeader1'][0] == 'TestData11'
        assert df['TestHeader1'][1] == 'TestData21'
        assert df['TestHeader2'][0] == 'TestData12'
        assert df['TestHeader2'][1] == 'TestData22'
        
    def test_pandas_rename_column(self):
        new_tape = Tape()
        new_tape.parse_tape_excel_file('test_files/simple_test_tape.xlsx')
        df = new_tape.data_frame
        df.rename(columns={'TestHeader1': 'Header1'}, inplace=True)
        assert df['Header1'][0] == 'TestData11'
        
        
    def test_standardize_column_names(self):
        new_tape = Tape()
        new_tape.parse_tape_config_file('test_files/simple_test_tape.ini')
        new_tape.parse_tape_excel_file('test_files/simple_test_tape.xlsx')
        new_tape.standardize_column_names()
        df = new_tape.data_frame
        assert df['Header1'][0] == 'TestData11'
        assert df['Header1'][1] == 'TestData21'
        assert df['Header2'][0] == 'TestData12'
        assert df['Header2'][1] == 'TestData22'