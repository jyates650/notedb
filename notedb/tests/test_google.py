"""Unit tests for the google URL creating module"""

from notedb.google import get_google_url, get_google_search_url, get_google_maps_url
from nose.tools import eq_

def test_get_google_url():
    """Test basic URL creation, with provided path, without website specified"""
    my_url = get_google_url('/somepath', 'my search TERMS')
    eq_(my_url, 'http://www.google.com/somepath?q=my+search+TERMS')

def test_get_google_url_website():
    """Test basic URL creation with provided path and provided website"""
    my_url = get_google_url('/ASDF', 'zaboomafoo', 'reddit.com')
    eq_(my_url, 'http://www.google.com/ASDF?q=zaboomafoo&sitesearch=reddit.com')

def test_get_google_search_url():
    """Test URL creation for google search, no provided website"""
    my_url = get_google_search_url('60 Pine Hill')
    eq_(my_url, 'http://www.google.com/search?q=60+Pine+Hill')

def test_get_search_url_website():
    """Test URL creation for google search, with provided website"""
    my_url = get_google_search_url('Chicago, IL 01234', 'trulia.com')
    eq_(my_url, 'http://www.google.com/search?q=Chicago%2C+IL+01234&sitesearch=trulia.com')

def test_get_google_map_url():
    """Test URL creation for google maps"""
    my_url = get_google_maps_url('540 R St, Sacramento, CA 95811')
    eq_(my_url, 'http://www.google.com/maps?q=540+R+St%2C+Sacramento%2C+CA+95811')
