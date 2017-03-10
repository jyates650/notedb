from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from notedb.database import Base

class Note(Base):
    __tablename__ = 'notes'
    id = Column(Integer, primary_key=True)
    address_id = Column(Integer, ForeignKey('addresses.id'))
    address = relationship("Address", back_populates="notes")