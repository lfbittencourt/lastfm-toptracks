# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import logging
import pandas as pd
import spotipy
import spotipy.util as util


class TrackPipeline(object):
    def open_spider(self, spider):
        self.items = []

    def close_spider(self, spider):
        if len(self.items) == 0:
            logging.warning('We have no items. Exiting...')
            return

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

        scope = 'user-library-read playlist-modify-private'
        token = util.prompt_for_user_token(
            spider.spotify_username,
            scope,
            client_id=spider.spotify_client_id,
            client_secret=spider.spotify_client_secret,
            redirect_uri='http://foo/'
        )

        if token:
            spotify = spotipy.Spotify(auth=token)
            track_ids = []

            for artist, row in df.iterrows():
                logging.info('Searching for %s - %s on Spotify...' % (
                    artist,
                    row['title']
                ))

                query = '"%s" artist:"%s"' % (row['title'], artist)
                results = spotify.search(q=query, type='track')

                if results['tracks']['total'] > 0:
                track_id = results['tracks']['items'][0]['id']

                logging.info('Found! ID is %s' % (track_id))
                track_ids.append(track_id)
                else:
                    logging.warning('%s - %s was not found' % (
                        artist,
                        row['title']
                    ))

            logging.info('Creating the playlist...')
            results = spotify.user_playlist_create(
                spider.spotify_username,
                'Last.fm %s - %s' % (spider.date_from, spider.date_to),
                public=False
            )

            playlist_id = results['id']
            playlist_url = results['external_urls']['spotify']

            logging.info('Created! ID is %s' % (playlist_id))
            logging.info('Adding tracks to the playlist...')

            results = spotify.user_playlist_add_tracks(
                spider.spotify_username,
                playlist_id,
                track_ids
            )

            logging.info('All done! Now just push play: %s' % (playlist_url))
        else:
            logging.error("Can't get token for %s" % (spider.spotify_username))

    def process_item(self, item, spider):
        self.items.append(item)

        return item
