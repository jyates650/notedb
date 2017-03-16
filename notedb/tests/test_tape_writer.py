import os
import pandas
import shutil
from notedb.tape import TapeWriter

class TestTapeWriter:
    
    tests_dir = os.path.dirname(os.path.abspath(__file__))
    temp_dir = os.path.join(tests_dir, 'temp')
    test_files_dir = os.path.join(tests_dir, 'test_files')
    
    def setUp(self):
        os.mkdir(self.temp_dir)
        
    def tearDown(self):
        shutil.rmtree(self.temp_dir)
        
    def test_write_dataframe_to_xls(self):
        pass
    
    def test_parse_template(self):
        pass
    
    def test_write_xls_no_template(self):
        pass
    
    def test_write_xls_with_template(self):
        pass
        