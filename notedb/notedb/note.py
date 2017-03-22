"""This module models a Note, which contains an Address"""

from notedb.google import get_google_maps_url, get_google_search_url

class Address:
    """Contains information regarding the address of a note"""
    
    def __init__(self, address, city, state, zipcode):
        self.address = address
        self.city = city
        self.state = state
        self.zipcode = zipcode

    def get_google_maps_url(self):
        """Return the Google Maps URL for this Address"""
        return get_google_maps_url(self.__str__())
    
    def get_trulia_url(self):
        """Return the trulia.com google search URL for this address"""
        return get_google_search_url(self.__str__(), website='trulia.com')

    def get_zillow_url(self):
        """Return the zillow.com google search URL for this address"""
        return get_google_search_url(self.__str__(), website='zillow.com')
   
    def __str__(self):
        return "{}, {}, {} {}".format(self.address, self.city, self.state, self.zipcode)
