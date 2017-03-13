import os
import notedb.main as main

class TestMain:
    
    def setUp(self):
        tests_dir = os.path.dirname(os.path.abspath(__file__))
        test_files_dir = os.path.join(tests_dir, 'test_files')
        self.simple_test_tape_ini = os.path.join(test_files_dir, 'simple_test_tape.ini')

    def test_config_parsing(self):
        config = main.parse_config_file(self.simple_test_tape_ini)
        col_map = config['column_mapping']
        assert col_map['Header1'] == 'TestHeader1'
        assert col_map['Header2'] == 'TestHeader2'
        for key, value in config['column_mapping'].items():
            assert col_map[key] == value