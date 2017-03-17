import os
import shutil

tests_dir = os.path.dirname(os.path.abspath(__file__))
temp_dir = os.path.join(tests_dir, 'temp')
test_files_dir = os.path.join(tests_dir, 'test_files')

def setup_package():
    os.mkdir(temp_dir)
    
def teardown_package():
    shutil.rmtree(temp_dir)