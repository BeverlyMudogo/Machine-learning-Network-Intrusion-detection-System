import os
from configparser import ConfigParser

def config(filename="/home/sakie/database.ini", section="railway"):
    """Fetch database configuration from environment variables or database.ini."""
    
    # Check if DATABASE_URL is available (for Railway deployment)
    database_url = os.getenv("DATABASE_URL")
    if database_url:
        return {"DATABASE_URL": database_url}  # Return as dictionary

    # Fallback: Read from database.ini for local development
    parser = ConfigParser()
    parser.read(filename)
    
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(f"Section {section} not found in {filename}")

    return db
