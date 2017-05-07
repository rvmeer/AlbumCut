# coding: utf-8

import spotipy
from pydub import AudioSegment
import requests
import os.path
import argparse

test = None
parser = argparse.ArgumentParser(description='Cuts a .wav file based on a Spotify album')
parser.add_argument('--artist', dest='artist_name', action='store', help='The artist name')
parser.add_argument('--album', dest='album_name', action='store', help='The album name')
parser.add_argument('--market', dest='market', action='store', help='The market (e.g. US)', default='NL')
parser.add_argument('--audio', dest='audio_filename', action='store', help='The audio filename (.wav format)')
args = parser.parse_args()

# artist_name = u'Daniël Lohues'.encode('utf-8')
artist_name = args.artist_name
# album_name = u'D'.encode('utf-8')
album_name = args.album_name

market = args.market or 'NL'

audio_file_path = None
if os.path.isabs(args.audio_filename):
    # audio_file_path = '/Users/lijn7tvshow/Documents/D.wav'
    audio_file_path = args.audio_filename
else:
    audio_file_path = os.path.abspath(args.audio_filename)

# Search for the artist in Spotify
spotify = spotipy.Spotify()
result = spotify.search(q='artist:{0}'.format(artist_name), type='artist')
artists = result['artists']['items']
artist = next(iter([artist for artist in artists if artist['name'].encode('utf-8') == artist_name]), None)
if not artist:
    print 'Artist {0} not found'.format(artist_name)
    exit()
artist_url = 'spotify:artist:{id}'.format(**artist)
print 'Artist found with Spotify: {0}'.format(artist_url)


class PagedResult(object):
    def __init__(self, spotify, result):
        self.spotify = spotify
        self.result = result
        self.items = None  # Lazy initialization

    def get_items(self):
        if self.items:
            return self.items

        self.items = self.result['items']

        while self.result['next']:
            self.result = self.spotify.next(self.result)
            self.items.extend(self.result['items'])

        return self.items


result = PagedResult(spotify, spotify.artist_albums(artist_url, album_type='album'))
album = next(iter([album for album in result.get_items() if
                   album['name'].encode('utf-8') == album_name and market.decode('utf-8') in (
                       album['available_markets'] or [])]), None)
if not album:
    print 'Album {0} for artist {1} not found'.format(album_name, artist_name)
    print 'Choose one of:'
    print '\n'.join(
        ['   {0} ({1})'.format(album['name'].encode('utf-8'), album['id']) for album in result.get_items() if
         market.decode('utf-8') in (album['available_markets'] or [])])
    exit()
print 'Album found with Spotify: {0}'.format(album['id'])

# Get the large cover image and write to cover_file_path
large_image = sorted(album['images'], key=lambda image: image['width'])[-1]
response = requests.get(large_image['url'])
filename = album_name
if response.headers['Content-Type'] == 'image/jpeg':
    filename = '{0}.jpg'.format(filename)
cover_file_path = os.path.join(os.path.dirname(audio_file_path), filename)
if os.path.isfile(cover_file_path):
    os.remove(cover_file_path)
cover_file = open(cover_file_path, "wb")
cover_file.write(response.content)
cover_file.close()
print 'Saved album cover to {0}'.format(cover_file_path)

# Load the audio
print 'Loading {0}'.format(audio_file_path)
audio = AudioSegment.from_file(audio_file_path, format="wav")

duration_in_ms = len(audio)
seconds = (duration_in_ms / 1000) % 60
minutes = (duration_in_ms / (1000 * 60)) % 60
hours = (duration_in_ms / (1000 * 60 * 60)) % 24
print 'Audio duration: {0:02d}:{1:02d}:{2:02d}'.format(hours, minutes, seconds)

# Write the tracks
tracks = PagedResult(spotify, spotify.album_tracks(album['id'])).get_items()
start_duration = 0
track_index = 1
for track in tracks:
    track_name = track['name'].encode('utf-8')
    track_duration = track['duration_ms']
    audio_track = audio[start_duration:start_duration + track_duration]
    track_file_name = "".join(i for i in track_name if i not in '\/:*?<>|')
    track_file_path = os.path.join(os.path.dirname(audio_file_path),
                                   '{0:02d} {1}.mp3'.format(track_index, track_file_name))

    print('Writing track {0}'.format(track_file_path))
    file_handle = audio_track.export(track_file_path,
                                     format='mp3',
                                     bitrate='320k',
                                     tags={'album': album['name'], 'artist': artist_name, 'track': track_index},
                                     cover=cover_file_path)

    track_index += 1
    start_duration += track_duration

    if start_duration > len(audio):
        print 'Audio file {0} is too short, terminating'.format(audio_file_path)
        exit()

print('All tracks exported successfully')
