#from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base


#user = 'root'
#password = 'bassfish'
#host = 'localhost'
#port = '3306'
#database = 'dev_notedb'

#engine = create_engine('mysql+mysqlconnector://root:bassfish@localhost/dev_notedb')

Base = declarative_base()
#Base.metadata.create_all(engine)