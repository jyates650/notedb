"""Module for connections to the Note Database"""

import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import InterfaceError, ProgrammingError

from notedb.common import NotedbUserError

Base = declarative_base()
class Database:
    """Responsible for connecting to the Note database"""
    
    def __init__(self):
        self.engine = None
        self.session = None
        self.connected = False

    def connect_to_database(self, flavor, user, passwd, host, db_name):
        """Attempt connecting to the database with the given credentials"""
        self.engine = create_engine('{}://{}:{}@{}/{}'.format(flavor, user, passwd, host, db_name))
        try:
            self.engine.connect()
        except InterfaceError:
            logging.warning('Could not connect to database. Is the host "%s" correct?', host)
            raise(NotedbUserError)
        except ProgrammingError:
            logging.warning('Could not connect to database. Check username, pass, and db_name.')
            raise(NotedbUserError)

        Session = sessionmaker()
        Session.configure(bind=self.engine)
        self.session = Session()
        self.connected = True
        logging.info('Successfully connected to the Database')

    def initialize_empty_database(self):
        """Create all necessary tables in an empty database
        NOTE: The tables to be created must be imported prior to running this method!
        """
        Base.metadata.create_all(self.engine)

db = Database()