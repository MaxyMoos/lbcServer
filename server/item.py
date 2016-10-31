# -*- coding: utf-8 -*-


class LeBonCoinItem(object):
	"""Represents an item displayed in LBC"""

	def __init__(self,
				 title=None,
				 price=None,
				 date=None,
				 location=None,
				 item_kind=None):
		"""Initialize instance"""
		if title is None:
			raise Exception("Cannot initialize a LeBonCoinItem without a title !")

		self.title = title
		self.priceStr = price
		self.dateStr = date
		self.location = location
		self.item_kind = item_kind