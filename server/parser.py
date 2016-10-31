# -*- coding: utf-8 -*-

class LeBonCoin_HTMLParser(object):
	"""Parses the HTML contents passed to it and builds list of items"""

	def get_items_from_HTML(html_contents):
		"""Get all items from the `html_contents` input

		`html_contents` must be a BeautifulSoup-parsed HTML instance
		"""
		if html_contents is None:
			raise Exception("Empty HTML passed to get_items_from_HTML !")

		itemElements = html_contents.body.find_all('section',
												   attrs={'class': 'item_infos'})


	def create_item_from_HTML(item_html):
		"""Create a single LBCItem instance from the HTML"""
		
		item_title = item_html.h2.text.strip()
		item_price = item_html.h3.text.strip()
		other_info = item_html.find_all('p',
										attrs={'class': 'item_supp'})

		# This assumes that there will *always* be 3 items in the list. Dangerous.
		item_kind = other_info[0].text.strip()
		item_location = other_info[1].text.strip()
		item_date = other_info[2].text.strip()

		