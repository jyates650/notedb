import logging
import pandas
import sys
from openpyxl import load_workbook
from notedb.common import NotedbUserError
from xlrd import XLRDError
       
class Tape:
    """Responsible for storing Tape Data"""
    
    def __init__(self):
        self.dataframe = None
        
    def read_xls(self, input_xls):
        """Read a Tape excel file and save as a DataFrame"""
        try:
            self.dataframe = pandas.read_excel(input_xls)
        except FileNotFoundError:
            raise NotedbUserError('Input file not found: %s', input_xls)
        except XLRDError:
            raise NotedbUserError('Input file format not supported. Is it excel?: %s', input_xls)
        logging.info('Tape data parsed from %s', input_xls)
            
    def write_xls(self, output_xls, template_xls=None):
        """Write Tape DataFrame to excel file. Use excel output template if provided"""
        tape_writer = TapeWriter()
        tape_writer.write_xls(self.dataframe, output_xls, template_xls)


class TapeFormatter:
    """Responsible for formating the columns of a Tape DataFrame"""
    
    def __init__(self, dataframe):
        self.dataframe = dataframe
        
    def rename_column(self, old_name, new_name):
        """Replace the old column name with a new name"""
        if old_name in self.dataframe.columns:
            self.dataframe.rename(columns = {old_name: new_name}, inplace=True)
            logging.info('Tape column %s renamed to %s', old_name, new_name)
        else:
            raise NotedbUserError('Unable to rename column %s: not found in DataFrame', old_name)
    
    def create_column(self, name, values):
        """Create a new column with initial values. Error if column already exists"""
        if name in self.dataframe.columns:
            raise NotedbUserError('Unable to create new column %s: column already exists', name)
        else:
            self.dataframe[name] = values
        
    def format_tape_columns(self, csv, format_name):
        """Change the tape DataFrame columns according to the format specified in the csv.
        
        The first row of the CSV contains the desired column names in the desired order.
        
        The first column of the CSV is the format_name label, used to specify a format for a
        given Tape. This column is not included when mapping names.
        """
        tape_formats_df = pandas.read_csv(csv)
        tape_format = self._get_tape_format(tape_formats_df, format_name)
        self._rename_or_add_columns(tape_format)
        self._reorder_columns(tape_format.keys())
        logging.info('Tape column formatting completed')
           
    def _get_tape_format(self, formats_df, format_name):    
        """Return the series of header mappings specified in the formats_df by the format_name"""  
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
        """Reorder the Tape DataFrame columns to match the column order provided"""
        self.tape_df = self.tape_df[column_order]
        logging.info('Tape columns reordered')
        

class TapeWriter:
    """Responsible for writing Tape data to an excel file, with support for an output template"""
    
    def __init__(self):
        self.tape_df = None
        self.template_df = None
        self.writer = None
        
    def write_xls(self, tape_df, output_xls, template_xls=None):
        """Write Tape DataFrame to excel file. Use excel output template if provided"""
        self.tape_df = tape_df
        self.writer = pandas.ExcelWriter(output_xls, engine='openpyxl')
        
        if template_xls:
            self._parse_template(template_xls)
            self._populate_template_with_tape_data()
            self._write_dataframe_to_xls(self.template_df, output_xls)
        else:
            self._write_dataframe_to_xls(self.tape_df, output_xls)
        
    def _parse_template(self, template_xls):
        """Read template xls. Save the data and sheets in TapeWriter"""
        try:
            self.template_df = pandas.read_excel(template_xls)
        except FileNotFoundError:
            raise NotedbUserError('Unable to find template file: %s', template_xls)
        logging.info('Loaded template: %s', template_xls)
        
        # Make sure other sheets in the template are copied
        book = load_workbook(template_xls)
        self.writer.book = book
        self.writer.sheets = dict((ws.title, ws) for ws in book.worksheets)
        
    def _populate_template_with_tape_data(self):
        """Populate the template DataFrame with matching columns in the Tape DF"""
        try:
            for col in self.template_df.columns:
                self.template_df[col] = self.tape_df[col]
        except KeyError:
            logging.warning('Could not find column %s in tape while copying to template', col)
        logging.info('Finished populating the Template with Tape data')
        
    def _write_dataframe_to_xls(self, dataframe, output_xls):
        """Write the DataFrame to an excel file"""
        # TODO add try/except block
        dataframe.to_excel(self.writer, index=False) # Don't write the index column
        self.writer.save()
        logging.info('Tape written to file %s', output_xls)
