import pandas
from xlrd import XLRDError
from pandas.io.common import CParserError


class NotedbUserError(Exception):
    pass


def get_dataframe_from_csv(csv_file):
    """Return a pandas DataFrame from the provided CSV file"""
    try:
        df = pandas.read_csv(csv_file)
        return df.fillna('') # Replace NaN values with empty string
    except FileNotFoundError:
        raise NotedbUserError('Input file not found: %s', csv_file)
    except CParserError:
        raise NotedbUserError('File format not supported. Is it CSV?: %s', csv_file)

def get_dataframe_from_xls(xls_file):
    """Return a pandas DataFrame from the provided Excel file"""
    try:
        df = pandas.read_excel(xls_file)
        return df.fillna('') # Replace NaN values with empty string
    except FileNotFoundError:
        raise NotedbUserError('Input file not found: %s', xls_file)
    except XLRDError:
        raise NotedbUserError('File format not supported. Is it excel?: %s', xls_file)