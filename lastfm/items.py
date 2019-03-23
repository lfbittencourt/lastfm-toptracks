# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Track(scrapy.Item):
    artist = scrapy.Field()
    title = scrapy.Field()
    scrobbles = scrapy.Field()
    first_scrobble = scrapy.Field()
    last_scrobble = scrapy.Field()
    scrobbles_per_day = scrapy.Field()
