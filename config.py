import os
from configparser import ConfigParser

def config(filename="database.ini", section="postgresql"):
    # Get the absolute path of the script's directory
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Construct the full path to database.ini
    file_path = os.path.join(base_dir, filename)

    # Create a parser
    parser = ConfigParser()
    
    # Read config file
    parser.read(file_path)
    db = {}

    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(
            "Section {0} not found in the {1} file".format(section, file_path)
        )
    
    return db
