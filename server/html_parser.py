# -*- coding: utf-8 -*-

"""Includes all necessities to parse HTML pages from LBC."""

from datetime import datetime, timedelta

from item import LeBonCoinItem


class LeBonCoin_HTMLParser(object):
    """Parses the HTML contents passed to it and builds list of items."""

    def get_items_from_HTML(self, html_contents):
        """Get all items from the `html_contents` input.

        `html_contents` must be a BeautifulSoup-parsed HTML instance
        """
        if html_contents is None:
            raise Exception("Empty HTML passed to get_items_from_HTML !")

        items = []

        urlElements = html_contents.body.find_all('a',
                                                  attrs={'class': "list_item clearfix trackable"})

        for item_html in urlElements:
            newItem = self.create_item_from_HTML(item_html)
            if newItem is not None:
                items.append(newItem)
        return items

    def get_datetime_from_string(self, date_string):
        """Parse the date string from LBC and return a corresponding datetime instance."""
        monthsInfo = {
            'jan':          1,
            'fév':          2,
            'mars':         3,
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

            if "Urgent" in str_elements[0]:
                str_elements = str_elements[1:]
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
        """Create a single LBCItem instance from the HTML."""
        item_url = 'http:' + item_html.attrs['href']
        item_html = item_html.section

        if item_html.h2:
            item_title = item_html.h2.text.strip()
        else:
            return None
        if item_html.h3:
            item_price = item_html.h3.text.strip()
        else:
            item_price = None
        other_info = item_html.find_all('p',
                                        attrs={'class': 'item_supp'})

        # This assumes that there will *always* be 3 items in the list. Dangerous.
        item_kind = other_info[0].text.strip()
        item_location = other_info[1].text.strip()
        if '/' in item_location:
            # Remove extra spaces
            item_location = " - ".join([item.strip() for item in item_location.split('/')])
        item_date = other_info[2].text.strip()

        item_dateStr = item_date
        item_date = self.get_datetime_from_string(item_date)

        item = LeBonCoinItem(item_title,
                             item_price,
                             item_url,
                             item_date,
                             item_dateStr,
                             item_location,
                             item_kind)
        return item
