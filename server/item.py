# -*- coding: utf-8 -*-

"""Defines the structure of a single LBC item."""

class LeBonCoinItem(object):
    """Represents an item displayed in LBC."""

    def __init__(self,
                 title=None,
                 price=None,
                 date=None,
                 location=None,
                 item_kind=None):
        """Initialize instance."""
        if title is None:
            raise Exception("Cannot initialize a LeBonCoinItem without a title !")

        self.title = title
        self.priceStr = price
        self.dateStr = date
        self.location = location
        self.item_kind = item_kind

    def __repr__(self):
        """A clearer representation of the class in console outputs."""
        return "<{} | {} | {} | {}>".format(self.title,
                                            self.priceStr,
                                            self.dateStr,
                                            self.location)
