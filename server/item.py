# -*- coding: utf-8 -*-

"""Defines the structure of a single LBC item."""

import json


class LeBonCoinItem(object):
    """Represents an item displayed in LBC."""

    def __init__(self,
                 title=None,
                 price=None,
                 url=None,
                 date=None,
                 dateStr=None,
                 location=None,
                 item_kind=None):
        """Initialize instance."""
        if title is None:
            raise Exception(
                "Cannot initialize a LeBonCoinItem without a title!"
            )

        if url is None:
            raise Exception(
                "Cannot initialize a LeBonCoinItem without an URL!"
            )

        self.title = title
        self.url = url
        self.priceStr = price
        self.date = date
        self.dateStr = dateStr
        self.location = location
        self.item_kind = item_kind

    def __repr__(self):
        """A clearer representation of the class in console outputs."""
        return "<{} | {} | {} | {}>".format(self.title,
                                            self.priceStr,
                                            self.dateStr,
                                            self.location)

    def to_json(self):
        fields_to_export = ['title',
                            'url',
                            'priceStr',
                            'dateStr',
                            'location',
                            'item_kind']

        d = {}
        for field in fields_to_export:
            d[field] = getattr(self, field)
        return json.dumps(d)
