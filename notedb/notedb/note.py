"""Contains all data and functions relating to a Note"""

from sqlalchemy import Column, Integer, String
from notedb.google import get_google_maps_url, get_google_search_url
from notedb.database import Base
import pandas

class Note(Base):
    """Contains all Note data, including the database interface"""
    __tablename__ = 'note'
    id = Column(Integer, primary_key=True)
    address = Column(String(100))
    city = Column(String(25))
    state = Column(String(2))
    zipcode = Column(Integer)

    REQUIRED_ARGS = ['address', 'city', 'state', 'zipcode']
    """These arguments are required to instantiate a new Note"""

    OPTIONAL_ARGS = []
    """These arguments can be optionally provided and will be saved to the DB"""

    UNSAVED_ARGS = ['google_maps_url', 'trulia_url', 'zillow_url']
    """These will not be saved to the DB, but may be useful for analysis"""

    def __init__(self, address, city, state, zipcode):
        self.address = address
        self.city = city
        self.state = state
        self.zipcode = zipcode

        # These will be automatically created from the address data
        self.google_maps_url = None
        self.trulia_url = None
        self.zillow_url = None
        self._create_google_urls()

    def get_address(self):
        """Return the full address of the Note in a string"""
        return '{}, {}, {} {:05d}'.format(self.address, self.city, self.state, self.zipcode)
    
    def as_pandas_series(self):
        """Return the contents of the Note as a Pandas Series object"""
        series_data = {}
        for key in (self.REQUIRED_ARGS + self.OPTIONAL_ARGS + self.UNSAVED_ARGS):
            series_data[key] = self.__dict__[key]
        return pandas.Series(series_data)

    def _create_google_urls(self):
        """Create all Google Search URLs based on the address and save them"""
        address = self.get_address()
        self.google_maps_url = get_google_maps_url(address)
        self.trulia_url = get_google_search_url(address, website='trulia.com')
        self.zillow_url = get_google_search_url(address, website='zillow.com')
