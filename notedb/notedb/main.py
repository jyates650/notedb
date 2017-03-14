import argparse
import configparser
import logging


from notedb.tape import TapeParser

def main():
    args = get_cmdline_arguments()
    init_logging(args)
    
    tape_parser = TapeParser(args.input_tape)
    
    if args.output_tape:
        tape_parser.write_tape_xls(args.output_tape)

def get_cmdline_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input-tape', required=True, type=argparse.FileType('w'),
                        help='Input tape xls file')
    parser.add_argument('-o', '--output-tape', type=argparse.FileType('w'),
                        help='Write formatted tape xls here')
    parser.add_argument('-v', '--verbose', action='store_true', help='Increase logging verbosity')
    parser.add_argument('-l', '--log-file', type=argparse.FileType('w'), help='Output log file')
    parser.add_argument('--format-csv', help='Tape formatting CSV', type=argparse.FileType('r'))
    parser.add_argument('--format-name', help='Tape format name within CSV')
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

def parse_config_file(config_file):
        config = configparser.ConfigParser()
        config.optionxform = str # Prevents automatic lower-casing of params
        config.read(config_file)
        return config
        
if __name__ == '__main__':
    main()