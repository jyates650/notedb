"""Simple script to create all necessary database tables"""

import os
import sys

# The notedb package is up one directory
libpath = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..')
sys.path.insert(1, libpath)

from notedb.database import db
from notedb.note import Note

db.connect_to_database('mysql+mysqlconnector', 'root', 'bassfish', 'localhost', 'dev_notedb')
db.initialize_empty_database()
