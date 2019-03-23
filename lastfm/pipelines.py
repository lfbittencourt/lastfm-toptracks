# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import logging
import pandas as pd


class TrackPipeline(object):
    def open_spider(self, spider):
        self.items = []

    def close_spider(self, spider):
        logging.info('Alright! Now we have %d track(s) to sort' % (
            len(self.items)
        ))

        df = pd.DataFrame \
               .from_dict(self.items) \
               .sort_values(
                   by=['scrobbles_per_day', 'first_scrobble'],
                   ascending=[False, True]
               ) \
               .groupby('artist', sort=False) \
               .agg({
                   'title': 'first',
                   'first_scrobble': 'first',
                   'scrobbles_per_day': sum,
               }) \
               .sort_values(by='scrobbles_per_day', ascending=False) \
               .head(30) \
               .sort_values(by='first_scrobble')

        logging.info('Sorting is done! Here are the chosen tracks:')

        counter = 0

        for artist, row in df.iterrows():
            counter += 1

            logging.info('%d) %s - %s' % (counter, artist, row['title']))

    def process_item(self, item, spider):
        self.items.append(item)

        return item
