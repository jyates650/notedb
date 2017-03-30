"""Unit tests for the database module"""

from nose.tools import raises

from notedb.database import Database
from notedb.common import NotedbUserError


def test_connect_to_database():
    """Test connection to database"""
    mydb = Database()
    mydb.connect_to_database('mysql+mysqlconnector', 'root', 'bassfish', 'localhost', 'dev_notedb')
    
@raises(NotedbUserError)
def test_connection_bad_host():
    """Test connecting with bad host name raises exception"""
    mydb = Database()
    mydb.connect_to_database('mysql+mysqlconnector', 'root', 'bassfish', 'bogus', 'dev_notedb')

@raises(NotedbUserError)
def test_connection_bad_user():
    """Test connecting with bad user name raises exception"""
    mydb = Database()
    mydb.connect_to_database('mysql+mysqlconnector', 'bogus', 'bassfish', 'localhost', 'dev_notedb')

@raises(NotedbUserError)
def test_connection_bad_pass():
    """Test connecting with bad pass raises exception"""
    mydb = Database()
    mydb.connect_to_database('mysql+mysqlconnector', 'root', 'bogus', 'localhost', 'dev_notedb')

@raises(NotedbUserError)
def test_connection_bad_dbname():
    """Test connecting with bad database name raises exception"""
    mydb = Database()
    mydb.connect_to_database('mysql+mysqlconnector', 'root', 'bassfish', 'localhost', 'bogus')
