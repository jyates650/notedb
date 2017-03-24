"""Unit tests for the note module"""

from notedb.note import Address
from nose.tools import eq_

class TestAddress:
    """Unit test class for the Address class"""

    addr = Address('345 H St.', 'Sacramento', 'CA', 95811)

    def test_address_string(self):
        """Test the Address class __str__ function"""
        eq_(str(self.addr), '345 H St., Sacramento, CA 95811')

    def test_google_maps_url(self):
        """Test getting google maps url for the address"""
        my_url = self.addr.get_google_maps_url()
        eq_(my_url, 'http://www.google.com/maps?q=345+H+St.%2C+Sacramento%2C+CA+95811')

    def test_trulia_url(self):
        """Test getting trulia URL for the address"""
        my_url = self.addr.get_trulia_url()
        eq_(my_url, 'http://www.google.com/search?q=345+H+St.%2C+Sacramento%2C+CA+95811'
            '&sitesearch=trulia.com')

    def test_zillow_url(self):
        """Test getting zillow URL for the address"""
        my_url = self.addr.get_zillow_url()
        eq_(my_url, 'http://www.google.com/search?q=345+H+St.%2C+Sacramento%2C+CA+95811'
            '&sitesearch=zillow.com')

def test_kwargs_instantiation():
    """Test the ability to instantiate Address using REQUIRED_ARGS and kwargs"""
    my_dict = {'address': '3 Green St', 'state': 'PA', 'zipcode': 39573, 'city': 'Kent', 's': 1}
    my_args = {}
    for arg in Address.REQUIRED_ARGS:
        my_args[arg] = my_dict[arg]
    my_addr = Address(**my_args)
    eq_(str(my_addr), '3 Green St, Kent, PA 39573')
