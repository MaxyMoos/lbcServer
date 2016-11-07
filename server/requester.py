# -*- coding: utf-8 -*-

"""All the necessary classes/methods to send regular requests to LBC website."""

from bs4 import BeautifulSoup

import unicodedata
import platform
from collections import OrderedDict
from urllib.request import urlopen


# Select relevant HTML parser depending on the current OS
curOS = platform.system()
if curOS == "Windows":
    BS_PARSER = "html.parser"
else:
    BS_PARSER = "lxml"


class LeBonCoin_UrlRequester(object):
    """The object that repeatedly makes the HTTP requests to LeBonCoin."""

    LBC_BASE_URL = "http://www.leboncoin.fr"
    LBC_STANDARD_SUFFIX = "/annonces/offres"

    LBC_FRENCH_REGIONS = OrderedDict([
                                        ('France', '/occasions/'),
                                        ('Paris', '/ile_de_france/paris'),
                                        ('Île-de-France', '/ile_de_france'),
                                        ('Alsace', '/alsace')
                                     ])

    # th=0 disables thumbnails so the HTML response is as small as possible
    LBC_SEARCH_PARAMS = "?f=a&th=0&q="

    def __init__(self,
                 search_query=None,
                 region=None,
                 search_interval=300):
        """Initialize instance."""
        self._validate_inputs(search_query, region, search_interval)
        self.search_query = search_query
        self.region = region
        self.search_interval = search_interval
        self._build_URL()

    def _validate_inputs(self, search_query, region, search_interval):
        """Check inputs and throws an Exception if they are not OK."""
        err_msg = []
        if search_query is None:
            err_msg += ["No search query entered"]
        if region is None:
            err_msg += ["No region entered"]
        elif region not in self.LBC_FRENCH_REGIONS.keys():
            err_msg += ["Invalid region entered: {}".format(region)]
        if search_interval < 0:
            err_msg += ["{}s is not a valid search interval".format(search_interval)]

        if len(err_msg) > 0:
            raise Exception('\n'.join(err_msg))

    @property
    def URL_formatted_search_query(self):
        """Remove accents in query and transform spaces in '+' signs."""
        tmpBytes = unicodedata.normalize('NFD', self.search_query).encode('ascii', 'ignore')
        tmpStr = tmpBytes.decode('utf-8')
        # Replace spaces by '+'
        tmpStr = tmpStr.replace(' ', '+')
        return tmpStr

    def _build_URL(self):
        """Build the URL. Yes."""
        self.url = self.LBC_BASE_URL + \
            self.LBC_STANDARD_SUFFIX + \
            self.LBC_FRENCH_REGIONS[self.region] + \
            self.LBC_SEARCH_PARAMS + \
            self.URL_formatted_search_query

    def get_HTML(self):
        """Query LeBonCoin and returns the HTML document."""
        f = urlopen(self.url)
        return BeautifulSoup(f, BS_PARSER)
