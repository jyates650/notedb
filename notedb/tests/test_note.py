"""Unit tests for the note module"""

import copy
import pandas
from pandas.util.testing import assert_series_equal
from notedb.note import Note
from nose.tools import eq_


class TestNote:
    """Unit test class for the Note class"""
    data = {
        'address': '345 H St.',
        'city': 'Sacramento',
        'state': 'CA',
        'zipcode': 5811
    }
    note = Note('345 H St.', 'Sacramento', 'CA', 5811)

    def test_get_address(self):
        """Test the get_address function"""
        eq_(self.note.get_address(), '345 H St., Sacramento, CA 05811')

    def test_create_urls(self):
        """Test the function that creates all the URLs"""
        my_note = copy.deepcopy(self.note)
        my_note.google_maps_url = None
        my_note.trulia_url = None
        my_note.zillow_url = None
        my_note._create_google_urls()
        eq_(my_note.google_maps_url, 'http://www.google.com/maps?q=345+H+St.%2C+'
            'Sacramento%2C+CA+05811')
        eq_(my_note.trulia_url, 'http://www.google.com/search?q=345+H+St.%2C+'
            'Sacramento%2C+CA+05811&sitesearch=trulia.com')
        eq_(my_note.zillow_url, 'http://www.google.com/search?q=345+H+St.%2C+'
            'Sacramento%2C+CA+05811&sitesearch=zillow.com')

    def test_as_pandas_series(self):
        """Test the function that returns the object as a pandas series"""
        maps_url = ('http://www.google.com/maps?q=345+H+St.%2C+'
                'Sacramento%2C+CA+05811')
        trul_url = ('http://www.google.com/search?q=345+H+St.%2C+'
                    'Sacramento%2C+CA+05811&sitesearch=trulia.com')
        zill_url = ('http://www.google.com/search?q=345+H+St.%2C+'
                    'Sacramento%2C+CA+05811&sitesearch=zillow.com')
        my_data = copy.deepcopy(self.data)
        my_data['google_maps_url'] = maps_url
        my_data['trulia_url'] = trul_url
        my_data['zillow_url'] = zill_url
        my_series = pandas.Series(my_data)
        assert_series_equal(self.note.as_pandas_series(), my_series, check_index_type=False)

def test_kwargs_instantiation():
    """Test the ability to instantiate Note using REQUIRED_ARGS and kwargs"""
    my_dict = {'address': '3 Green St', 'state': 'PA', 'zipcode': 39573, 'city': 'Kent', 's': 1}
    my_args = {}
    for arg in Note.REQUIRED_ARGS:
        my_args[arg] = my_dict[arg]
    my_note = Note(**my_args)
    eq_(my_note.get_address(), '3 Green St, Kent, PA 39573')
