# -*- coding: utf-8 -*-

from datetime import datetime

from item import LeBonCoinItem


class LeBonCoin_HTMLParser(object):
	"""Parses the HTML contents passed to it and builds list of items"""

	def get_items_from_HTML(self, html_contents):
		"""Get all items from the `html_contents` input

		`html_contents` must be a BeautifulSoup-parsed HTML instance
		"""
		if html_contents is None:
			raise Exception("Empty HTML passed to get_items_from_HTML !")

		items = []
		itemElements = html_contents.body.find_all('section',
												   attrs={'class': 'item_infos'})
		for item_html in itemElements:
			items += [self.create_item_from_HTML(item_html)]
		return items

	def get_datetime_from_string(self, date_string):
	    monthsInfo = {
	        'jan':          1,
	        'fév':          2,
	        'mar':          3,
	        'avr':          4,
	        'mai':          5,
	        'juin':         6,
	        'juil':         7,
	        'août':         8,
	        'sept':         9,
	        'oct':          10,
	        'nov':          11,
	        'déc':          12
	    }

	    if date_string:
	        str_elements = [i.strip() for i in date_string.split()]

	        if "Aujourd'hui" in str_elements[0]:
	            day = datetime.now().day
	            month = datetime.now().month
	        elif "Hier" in str_elements[0]:
	            yday = datetime.now() - timedelta(days=1)
	            day = yday.day
	            month = yday.month
	        else:
	        	day = int(str_elements[0])
	        	month = monthsInfo[str_elements[1][:-1]]

	        hour = int(str_elements[-1][0:2])
	        minutes = int(str_elements[-1][3:5])

	        return datetime(datetime.today().year,
	                        month,
	                        day,
	                        hour=hour,
	                        minute=minutes)

	def create_item_from_HTML(self, item_html):
		"""Create a single LBCItem instance from the HTML"""
		
		item_title = item_html.h2.text.strip()
		item_price = item_html.h3.text.strip()
		other_info = item_html.find_all('p',
										attrs={'class': 'item_supp'})

		# This assumes that there will *always* be 3 items in the list. Dangerous.
		item_kind = other_info[0].text.strip()
		item_location = other_info[1].text.strip()
		item_date = other_info[2].text.strip()

		item_date = self.get_datetime_from_string(item_date)

		item = LeBonCoinItem(item_title,
							 item_price,
							 item_date,
							 item_location,
							 item_kind)
