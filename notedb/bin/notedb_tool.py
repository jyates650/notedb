__author__ = 'Jeff Yates (jyates650@gmail.com)'

import argparse
import logging
import os
import sys
from notedb.common import NotedbUserError

# The notedb package is up one directory
libpath = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..')
sys.path.insert(1, libpath)

from notedb.tape import Tape

def main():
    args = get_cmdline_arguments()
    init_logging(args)
    
    my_tape = Tape()
    
    my_tape.read_xls(args.input_tape)
    
    if args.format_csv:
        my_tape.format_columns_from_csv(args.format_csv)
    
    if args.output_tape:
        my_tape.write_xls(args.output_tape, args.template_xls)

def get_cmdline_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input-tape', required=True, help='Input tape xls file')
    parser.add_argument('-o', '--output-tape', help='Write formatted tape xls here')
    parser.add_argument('-v', '--verbose', action='store_true', help='Increase logging verbosity')
    parser.add_argument('-l', '--log-file', help='Output log file')
    parser.add_argument('-t', '--template-xls', help='Tape output template file to populate')
    parser.add_argument('--format-csv', help='Tape formatting CSV')
    return parser.parse_args()

def init_logging(args):
    level = logging.INFO
    if args.verbose:
        level = logging.DEBUG
        
    log_format = '%(levelname)s: %(message)s'
    
    if (args.log_file):
        logging.basicConfig(level=level, format=log_format, filename=args.log_file, filemode='w')
    else:
        logging.basicConfig(level=level, format=log_format)
        
if __name__ == '__main__':
    try:
        main()
    except NotedbUserError as e:
        logging.error(e)
        logging.error('Notedb tool has failed')
        sys.exit(1)
    except Exception: # pylint: disable=broad-except
        logging.exception('Something bad happened')
        logging.error('Please contact %s. He will need to fix this', __author__)
        sys.exit(2)