import pandas as pd

class Tape:

    def __init__(self, config):
        self.config = config
        
    def parse_tape_excel_file(self, excel_file):
        self.data_frame = pd.read_excel(excel_file)
        
    def standardize_column_names(self):
        for standard_name, excel_name in self.config['column_mapping'].items():
            print(standard_name)
            print(excel_name)
            self.data_frame.rename(columns={excel_name: standard_name}, inplace=True)