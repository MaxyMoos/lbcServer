# -*- coding: utf-8 -*-


class LeBonCoinItem(object):
	"""Represents an item displayed in LBC"""

	def __init__(self,
				 title=None,
				 price,
				 date,
				 location,
				 item_kind):
		"""Initialize instance"""
		if title is None:
			raise Exception("Cannot initialize a LeBonCoinItem without a title !")

		self.title = title
		self.priceStr = price
		self.dateStr = date
		self.location = location
		self.item_kind = item_kind