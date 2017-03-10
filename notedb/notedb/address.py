from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from notedb.database import Base

class Address(Base):
    __tablename__ = 'addresses'
    id = Column(Integer, primary_key=True)
    notes = relationship('Note', back_populates="addresses")