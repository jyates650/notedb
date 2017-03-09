import notedb.main as main

class TestMain:

    def test_config_parsing(self):
        config = main.parse_config_file('tests/test_files/simple_test_tape.ini')
        col_map = config['column_mapping']
        assert col_map['Header1'] == 'TestHeader1'
        assert col_map['Header2'] == 'TestHeader2'
        for key, value in config['column_mapping'].items():
            assert col_map[key] == value