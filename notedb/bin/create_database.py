"""Simple script to create all necessary database tables"""

import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# The notedb package is up one directory
libpath = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..')
sys.path.insert(1, libpath)

from notedb.note import Address
from notedb.database import Base

engine = create_engine('mysql+mysqlconnector://root:bassfish@localhost/dev_notedb')
Base.metadata.create_all(engine)
