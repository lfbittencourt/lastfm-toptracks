# Last.fm tracks of the year

I love music and I love lists. As Last.fm is some kind of intersection between
these two passions, I keep my account updated with almost every digital music
I've been listening to since 2006. Yup, 13 years.

Every December, I like to make a playlist with the top tracks I've listened to
during the year. Spotify already does something similar, but it's not that right
and I know it because of Last.fm data. Besides that, it's very fun to do your
own mixtapes, right?

This crawler does exactly this. It takes a year, scrape Last.fm tables to
retrieve its top tracks and creates a Spotify playlist. To make things funnier,
I have some personal rules to sort the songs and choose the ones that will end
up in the playlist:

- Tracks **discovered** that year shall be prioritized
- The playlist must contain only one track per artist, but the artists that appear more than once score extra   points
- To create a sense of timeline, the songs must be sorted by "discovery" date

## Requisites

- [Python 3](https://www.python.org/downloads/)
- [Scrapy](https://scrapy.org/download/)
- [pandas](https://pandas.pydata.org/)
- [Spotipy](https://spotipy.readthedocs.io/en/latest/)

As track searching and playlist creation require Spotify authentication, you'll
have to create [a Spotify application](https://developer.spotify.com/dashboard/applications) too.

## How to run it

It's simple:

```
scrapy crawl toptracks -a lastfm_username=FOO -a spotify_username=FOO -a spotify_client_id=FOO -a spotify_client_secret=FOO
```

Don't forget to replace all the `FOO`s by valid information. The parameter names
are pretty straightforward and you won't have any difficulty filling them.

By default, the crawler searches for last year tracks and limit playlist to 30
tracks. To change that, use `year` and `playlist_length params`:

```
scrapy crawl toptracks ... -a year=2015 -playlist_length=50
```
