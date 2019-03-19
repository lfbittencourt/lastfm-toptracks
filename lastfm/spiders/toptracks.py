# -*- coding: utf-8 -*-
import logging
import scrapy
import re
from datetime import date, datetime
from lastfm.items import Track

class ToptracksSpider(scrapy.Spider):
    name = 'toptracks'
    date_from = date(2018, 1, 1)
    date_to = date(2018, 12, 31)
    start_urls = [
        'https://www.last.fm/user/Bittencourt/library/tracks?from=%s&to=%s' % (date_from, date_to),
        'https://www.last.fm/user/Bittencourt/library/tracks?from=%s&to=%s&page=2' % (date_from, date_to),
    ]

    def parse(self, response):
        for track_row in response.css('tr.js-link-block'):
            item = Track(
                artist = track_row.xpath('td[4]/span/span[1]/a/text()').get(),
                title = track_row.xpath('td[4]/span/a/text()').get(),
                scrobbles = int(track_row.xpath('td[7]/span/span/a/span[1]/text()').get().strip()),
            )

            logging.info('Crawling %s - %s...' % (item['artist'], item['title']))

            internal_url = track_row.xpath('td[7]/span/span/a/@href').get()
            internal_url = re.sub(r'&?from=\d{4}-\d{2}-\d{2}&?', '', internal_url) # remove "from" QS
            request = response.follow(internal_url, self.parse_internal)

            request.meta['item'] = item

            yield request

    def parse_internal(self, response):
        item = response.meta['item']

        if (item.get('last_scrobble') is None):
            last_scrobble = response.css('.chartlist tbody tr:first-child td:last-child span::text').get()
            last_scrobble = self.parse_date(last_scrobble)

            item['last_scrobble'] = last_scrobble

        last_page_link = response.css('ul.pagination-list a:last-child::attr(href)').get()

        if '?page=' not in response.url and last_page_link is not None:
            request = response.follow(last_page_link, self.parse_internal)

            request.meta['item'] = item

            yield request
            return

        first_scrobble = response.css('.chartlist tbody tr:last-child td:last-child span::text').get()
        first_scrobble = self.parse_date(first_scrobble)

        item['first_scrobble'] = first_scrobble

        delta = self.date_to - item['first_scrobble'].date()

        item['scrobbles_per_day'] = item['scrobbles'] / delta.days

        yield item

    def parse_date(self, date_string):
        time_formats = ['%d %b %Y, %I:%M%p', '%d %b %I:%M%p']

        try:
            # Example: 4 Nov 2018, 4:35pm
            date = datetime.strptime(date_string, time_formats[0])
        except:
            # Example: 12 Jan 8:51pm
            date = datetime.strptime(date_string, time_formats[1])

        if (date.year == 1900):
            now = datetime.now()
            fixed_year = now.year if date.strftime('%m%d') <= now.strftime('%m%d') else now.year - 1
            date = date.replace(year = fixed_year)

        return date
