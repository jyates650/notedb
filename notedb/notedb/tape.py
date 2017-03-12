from sqlalchemy import Column, Integer, Table, ForeignKey
from sqlalchemy.orm import relationship
from notedb.database import Base

import pandas as pd
    
tapes_notes_table = Table(
    'association', Base.metadata,
    Column('note_id', Integer, ForeignKey('notes.id')),
    Column('tape_id', Integer, ForeignKey('tapes.id'))
    )

class Tape(Base):
    __tablename__ = 'tapes'
    id = Column(Integer, primary_key=True)
    notes = relationship(
        'Note',
        secondary=tapes_notes_table,
        back_populates='tapes'
        )

class TapeParser:

    def __init__(self, config):
        self.config = config
        
    def parse_new_tape_xls(self, excel_file):
        self.data_frame = pd.read_excel(excel_file)
        
    def standardize_column_names(self):
        for standard_name, excel_name in self.config['column_mapping'].items():
            self.data_frame.rename(columns={excel_name: standard_name}, inplace=True)