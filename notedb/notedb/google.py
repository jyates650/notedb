"""Module for creating Google Search URLs"""

from urllib.parse import urlencode, urlunparse

SCHEME = 'http'
NETLOC = 'www.google.com'
PARAMS = ''
FRAGMENT = ''

def get_google_url(path, search_terms, website=None):
    """Return Google search URL for the given search terms and optional website.
    path for google maps is '/maps' and for search it is '/search'
    """
    query = [('q', search_terms)] # Use a list of tuple pairs to maintain the order of terms
    if website:
        query.append(('sitesearch', website))
    encoded_query = urlencode(query)
    url_components = (SCHEME, NETLOC, path, PARAMS, encoded_query, FRAGMENT)
    return urlunparse(url_components)

def get_google_search_url(search_terms, website=None):
    """Return the Google search URL for the given search terms and optional website."""
    return get_google_url('/search', search_terms, website)

def get_google_maps_url(search_terms):
    """Return the Google Maps search URL for the given terms and optional website."""
    return get_google_url('/maps', search_terms)
