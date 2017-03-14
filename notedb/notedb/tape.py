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
        
    def update_tape_headers_from_csv(self, csv, format_name):
        """Update the Tape column headers according to format in the CSV file."""
        tape_formats = pd.read_csv(csv)
        header_names = self._get_header_mapping_by_format(tape_formats, format_name)
        self._rename_or_add_tape_columns(header_names)
        
    def _get_header_mapping_by_format(self, tape_formats, format_name):
        """Return the header_mapping dictionary found by format_name in the tape_formats df."""
        for index, row in tape_formats.iterrows():
            if row[self.FORMAT_NAME_KEY] == format_name:
                return row # Choose first matching row
        
    def _rename_or_add_tape_columns(self, header_mapping):
        """Rename tape columns if a mapping exists, otherwise create new column."""
        for new_name, old_name in header_mapping.items():
            try:
                self.tape_df[new_name] = self.tape_df[old_name]
                del self.tape_df[old_name]
            except (KeyError, ValueError):
                if new_name is not self.FORMAT_NAME_KEY:
                    self.tape_df[new_name] = ''