import configparser

def main():
    pass

def parse_config_file(config_file):
        config = configparser.ConfigParser()
        config.optionxform = str # Prevents automatic lower-casing of params
        config.read(config_file)
        return config
        
if __name__ == '__main__':
    main()