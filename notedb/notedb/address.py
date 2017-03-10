from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from notedb.database import Base

class Address(Base):
    __tablename__ = 'addresses'
    id = Column(Integer, primary_key=True)
    notes = relationship('Note', back_populates="addresses")
    
    def get_google_street_view_link(self):
        pass
    
    def get_trulia_link(self):
        pass
    
    def get_crime_report_score(self):
        pass
    
    def standardize_address(self):
        pass
    
    def get_raw_address(self):
        pass