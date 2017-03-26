import logging
import pandas

from openpyxl import load_workbook
from notedb.common import NotedbUserError, get_dataframe_from_xls, get_dataframe_from_csv
from notedb.note import Address, Note      
      
class Tape:
    """Responsible for storing Tape Data"""
    
    def __init__(self):
        self.dataframe = None
        self.notes = []
        
    def read_xls(self, input_xls):
        """Read a Tape excel file and save as a DataFrame"""
        self.dataframe = get_dataframe_from_xls(input_xls)
        logging.info('Tape data parsed from %s', input_xls)
            
    def write_xls(self, output_xls, template_xls=None):
        """Write Tape DataFrame to excel file. Use excel output template if provided"""
        tape_writer = TapeWriter()
        tape_writer.write_xls(self.dataframe, output_xls, template_xls)
        
    def format_columns_from_csv(self, format_csv):
        """Format the Tape column headers according to the mapping in the CSV"""
        formatter = TapeFormatter(self.dataframe)
        formatter.format_columns_from_csv(format_csv)
        
    def populate_database_objects(self):
        """Instantiate the SQL database objects for this Tape"""
        for _, note_data in self.dataframe.iterrows():
            note = self._get_note_object(note_data)
            self.notes.append(note)

    def _get_note_object(self, note_data):
        """Return a Note object for the provided raw note_data"""
        args = {}
        for arg in Note.REQUIRED_ARGS:
            try:
                args[arg] = note_data[arg]
            except KeyError:
                raise NotedbUserError('Unable to find Column "{}" in the Tape.'.format(arg))
        return Note(**args)


class TapeFormatter:
    """Responsible for formating the columns of a Tape DataFrame"""
    
    def __init__(self, dataframe):
        self.dataframe = dataframe
        
    def rename_column(self, old_name, new_name):
        """Replace the old column name with a new name"""
        if old_name not in self.dataframe.columns:
            raise KeyError('Column %s not found in DataFrame', old_name)
        self.dataframe.rename(columns = {old_name: new_name}, inplace=True)
        logging.info('Tape column %s renamed to %s', old_name, new_name)
    
    def create_column(self, name, values=None):
        """Create a new column with initialized values. Error if column already exists"""
        if name in self.dataframe.columns:
            raise NotedbUserError('Unable to create new column %s: column already exists', name)
        else:
            self.dataframe[name] = values
            logging.info('Created new Tape column "%s" with values "%s"', name, values)
    
    def reorder_columns(self, column_order):
        """Reorder the tape columns based on the provided list of column headers"""
        self.dataframe = self.dataframe[column_order]
        logging.info('Tape columns reordered')
  
    def format_columns_from_map(self, format_map):
        """Rename or add new columns according to a {new_name: old_name} map"""
        for new_name, old_name in format_map.items():
            if new_name == old_name:
                continue
            try:
                self.rename_column(old_name, new_name)
            except KeyError:
                logging.info('Unable to find column "%s" to rename, creating a new one', old_name)
                self.create_column(new_name)
    
    def format_columns_from_csv(self, format_csv):
        """Rename or add new columns according to {new_name: old_name} map inside the CSV"""
        format_df = get_dataframe_from_csv(format_csv)
        # Assume first non-header line in CSV is the mapping data   
        format_map = format_df.iloc[0]
        self.format_columns_from_map(format_map)        


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
        self.template_df = get_dataframe_from_xls(template_xls)
        logging.info('Loaded template from file: %s', template_xls)
        
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
