# -*- coding: utf-8 -*-

import html_requester
import html_parser
import item

class LeBonCoin_QueryManager(object):
	"""Central manager for a single query - calls all from HTML request to putting items in DB"""

	def __init__(self, query, location, delay):
		"""Initialize instance"""
		self.query = query
		self.location = location
		self.delay = delay

		# Input validation happens on the next line
		self.requester = html_requester.LeBonCoin_UrlRequester(query, location, delay)
		self.parser = html_parser.LeBonCoin_HTMLParser()

	def run(self):
		"""Starts the process"""
		html = self.requester.get_HTML()
		items = self.parser.get_items_from_HTML(html)
