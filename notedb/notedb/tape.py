import configparser
import pandas as pd

class Tape:
    
    def parse_tape_config_file(self, config_file):
        self.config = configparser.ConfigParser()
        self.config.optionxform = str # Prevents automatic lower casing of ini
        self.config.read(config_file)
        
    def parse_tape_excel_file(self, excel_file):
        self.data_frame = pd.read_excel(excel_file)
        
    def standardize_column_names(self):
        for standard_name, excel_name in self.config['column_mapping'].items():
            print(standard_name)
            print(excel_name)
            self.data_frame.rename(columns={excel_name: standard_name}, inplace=True)