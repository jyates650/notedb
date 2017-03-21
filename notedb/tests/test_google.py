"""Unit tests for the google module"""

from notedb.google import get_google_url
from nose.tools import eq_

class TestGoogle ():

    
    def test_get_google_url(self):
        my_url = get_google_url('/somepath', 'my search TERMS')
        eq_(my_url, 'http://www.google.com/somepath?q=my+search+TERMS')
        
    def test_get_google_url_website(self):
        my_url = get_google_url('/ASDF', 'zaboomafoo', 'reddit.com')
        eq_(my_url, 'http://www.google.com/ASDF?q=zaboomafoo&sitesearch=reddit.com')
        