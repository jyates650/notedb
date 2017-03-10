from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base


user = 'root'
password = 'bassfish'
host = 'localhost'
port = '3306'
database = 'dev_notedb'

engine = create_engine('mysql+mysqlconnector://root:bassfish@localhost/dev_notedb', echo=True)


Base = declarative_base()

class Note(Base):
    __tablename__ = 'notes'
    
    id = Column(Integer, primary_key=True)
    
Base.metadata.create_all(engine)