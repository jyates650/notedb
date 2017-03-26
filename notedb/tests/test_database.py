from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from notedb.database import Base
import notedb.note

def test_database():
    engine = create_engine('mysql+mysqlconnector://root:bassfish@localhost/dev_notedb')
    Session = sessionmaker()
    Session.configure(bind=engine)
    Base.metadata.create_all(engine)
    #addr = Address('345 H St.', 'Sacramento', 'CA', 95811)
    ##session = Session()
    #session.add(addr)
    #session.commit()