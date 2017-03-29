"""Module for connections to the Note Database"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()engine = create_engine('mysql+mysqlconnector://root:bassfish@localhost/dev_notedb')
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()
