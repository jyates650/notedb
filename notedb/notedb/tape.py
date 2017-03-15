import logging
import pandas
import sys
from openpyxl import load_workbook

class TapeParser:
    
    FORMAT_NAME_KEY = 'TapeFormat'
    
    def __init__(self, input_tape_xls):
        self.tape_df = pandas.read_excel(input_tape_xls)
        logging.info('Tape parsed from %s', input_tape_xls)
        
    def get_tape_object(self):
        return Tape(self.tape_df)
        
    def format_tape_columns(self, csv, format_name):
        tape_formats_df = pandas.read_csv(csv)
        tape_format = self._get_tape_format(tape_formats_df, format_name)
        self._rename_or_add_columns(tape_format)
        self._reorder_columns(tape_format.keys())
        logging.info('Tape column formatting completed')
        
    def _get_tape_format(self, formats_df, format_name):      
        for index, row in formats_df.iterrows():
            if row[self.FORMAT_NAME_KEY] == format_name:
                del row[self.FORMAT_NAME_KEY] # Non-Data column
                return row # Choose first matching row
        logging.error('Column format "%s" not found')
        sys.exit()
        
    def _rename_or_add_columns(self, tape_format):
        """Rename tape columns if a mapping exists, otherwise create new column."""
        for new_name, old_name in tape_format.items():
            if new_name != old_name:
                try:
                    self.tape_df[new_name] = self.tape_df[old_name]
                    del self.tape_df[old_name]
                    logging.info('Tape column "%s" renamed to "%s"', old_name, new_name)
                except (KeyError, ValueError): # old_name column doesn't exist
                    self.tape_df[new_name] = ''
                    logging.info('New tape column "%s" created', new_name)
                    
    def _reorder_columns(self, column_order):
        self.tape_df = self.tape_df[column_order]
        logging.info('Tape columns reordered')


class Tape:
    
    def __init__(self, dataframe):
        self.dataframe = dataframe
            
    def write_xls(self, output_xls, template_xls=None):
        """Write Tape data to excel file. Populate data into template if provided"""
        if template_xls:
            self._write_xls_with_template(output_xls, template_xls)
        else:
            self._write_xls_without_template(output_xls)
        logging.info('Tape written to file %s', output_xls)
        
    def _write_xls_with_template(self, output_xls, template_xls):
        writer = pandas.ExcelWriter(output_xls)
        
        # Read in the template and populate with Tape data
        template_df = pandas.read_excel(template_xls)
        for col in self.dataframe.columns:
            template_df[col] = self.dataframe[col]
        
        # Make sure other sheets in the template don't get wiped out
        book = load_workbook(template_xls)
        writer.book = book
        writer.sheets = dict((ws.title, ws) for ws in book.worksheets)
        
        # Save the populated template DataFrame to the output file
        template_df.to_excel(writer, index=False)
        writer.save()
    
    def _write_xls_without_template(self, output_xls):
        writer = pandas.ExcelWriter(output_xls)
        self.dataframe.to_excel(writer, index=False)
        writer.save()
        