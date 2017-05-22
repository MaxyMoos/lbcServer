# -*- coding: utf-8 -*-

"""Defines the structure of a single LBC item."""

import json
import datetime


LBCITEM_JSON_IDENTIFIER = '__lbcitem__'


class BadJSONException(Exception):
    pass


class LeBonCoinItemJSONEncoder(json.JSONEncoder):
    """Encodes LeBonCoinItems to JSON"""

    def default(self, obj):
        """Encoding method"""
        if isinstance(obj, LeBonCoinItem):
            return obj.get_json_dict()
        else:
            return json.JSONEncoder.default(self, obj)


class LeBonCoinItemJSONDecoder(json.JSONDecoder):
    """Decodes JSON into LeBonCoinItems"""

    def __init__(self, *args, **kwargs):
        """Initialize instance"""
        json.JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, obj):
        """Custom decoder for LeBonCoinItems"""
        if LBCITEM_JSON_IDENTIFIER in obj.keys():
            return LeBonCoinItem.init_from_json(obj)
        else:
            return obj


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

    def get_json_dict(self, fields_to_export=None):
        """Get a JSON-friendly dictionary representation of the item"""
        if not fields_to_export:
            fields_to_export = ['title',
                                'url',
                                'priceStr',
                                'date',
                                'dateStr',
                                'location',
                                'item_kind']

        d = {LBCITEM_JSON_IDENTIFIER: True}
        for field in fields_to_export:
            if field == 'date':
                if self.date is not None:
                    d[field] = self.date.isoformat()
            else:
                d[field] = getattr(self, field)
        return d

    @classmethod
    def init_from_json(self, dict_item):
        """Initialize a new LeBonCoin item from a parsed JSON dict object"""

        item_keys = dict_item.keys()

        if 'title' not in item_keys:
            raise BadJSONException("Missing title info in source dict:\n{}".format(dict_item))
        if 'url' not in item_keys:
            raise BadJSONException("Missing URL info in source dict:\n{}".format(dict_item))

        title = dict_item['title']
        url = dict_item['url']
        price = dict_item.get('priceStr', None)
        dateStr = dict_item.get('dateStr', None)
        location = dict_item.get('location', None)
        item_kind = dict_item.get('item_kind', None)
        # Special handling for datetime
        try:
            date = datetime.datetime.strptime(dict_item.get('date', ''),
                                              '%Y-%m-%dT%H:%M:%S.%f')
        except ValueError:
            date = None

        return LeBonCoinItem(title, price, url, date, dateStr, location, item_kind)
