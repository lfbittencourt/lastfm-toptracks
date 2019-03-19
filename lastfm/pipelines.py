# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import logging

class TrackPipeline(object):
    def open_spider(self, spider):
        self.items = []

    def close_spider(self, spider):
        logging.debug(self.items)

    def process_item(self, item, spider):
        self.items.append(item)

        return item
