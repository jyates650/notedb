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
    
    FORMAT_NAME_KEY = 'TapeFormat'
    
    def __init__(self, input_tape_xls):
        self.tape_df = pd.read_excel(input_tape_xls)
        
    def write_tape_xls(self, output_tape_xls):
        writer = pd.ExcelWriter(output_tape_xls)
        self.tape_df.to_excel(writer)
        writer.save()
        
    def format_tape_columns(self, csv, format_name):
        tape_formats_df = pd.read_csv(csv)
        tape_format = self._get_tape_format(tape_formats_df, format_name)
        self._rename_or_add_columns(tape_format)
        self._reorder_columns(tape_format.keys())
        
    def _get_tape_format(self, formats_df, format_name):      
        for index, row in formats_df.iterrows():
            if row[self.FORMAT_NAME_KEY] == format_name:
                del row[self.FORMAT_NAME_KEY] # Non-Data column
                return row # Choose first matching row
        
    def _rename_or_add_columns(self, tape_format):
        """Rename tape columns if a mapping exists, otherwise create new column."""
        for new_name, old_name in tape_format.items():
            if new_name != old_name:
                try:
                    self.tape_df[new_name] = self.tape_df[old_name]
                    del self.tape_df[old_name]
                except (KeyError, ValueError):
                    self.tape_df[new_name] = ''
                    
    def _reorder_columns(self, column_order):
        self.tape_df = self.tape_df[column_order]