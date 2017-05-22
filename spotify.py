# coding: utf-8

import spotipy
import spotipy.util as util
from pydub import AudioSegment
import requests
import os.path
import argparse
import json
from slugify import slugify

username = None
client_id = None
client_secret = None
redirect_uri = None
with open('./albumcut_config.json', 'rb') as config_file:
    config = json.loads(config_file.read())
    username = config['username']
    client_id = config['client_id']
    client_secret = config['client_secret']
    redirect_uri = config['redirect_uri']


def get_artist_url(artist_name):
    # Search for the artist in Spotify
    spotify = spotipy.Spotify()
    result = spotify.search(q='artist:{0}'.format(artist_name), type='artist')
    artists = result['artists']['items']
    artist = next(iter([artist for artist in artists if artist['name'].encode('utf-8') == artist_name]), None)
    if not artist:
        return None
    return 'spotify:artist:{id}'.format(**artist)


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


def get_album(artist_url, album_name, market):
    spotify = spotipy.Spotify()
    result = PagedResult(spotify, spotify.artist_albums(artist_url, album_type='album'))
    album = next(iter([album for album in result.get_items() if
                       album['name'].encode('utf-8') == album_name and market.decode('utf-8') in (
                           album['available_markets'] or [])]), None)
    if not album:
        print 'Album {0} for artist {1} not found'.format(album_name, artist_url)
        print 'Choose one of:'
        print '\n'.join(
            ['   {0} ({1})'.format(album['name'].encode('utf-8'), album['id']) for album in result.get_items() if
             market.decode('utf-8') in (album['available_markets'] or [])])
        return None
    print 'Album found with Spotify: {0}'.format(album['id'])
    return album


def save_cover(album, folder):
    # Get the large cover image and write to cover_file_path
    large_image = sorted(album['images'], key=lambda image: image['width'])[-1]
    response = requests.get(large_image['url'])
    filename = slugify(album['name'].encode('utf-8'))
    if response.headers['Content-Type'] == 'image/jpeg':
        filename = '{0}.jpg'.format(filename)

    cover_file_path = os.path.join(folder, filename)
    if os.path.isfile(cover_file_path):
        os.remove(cover_file_path)
    cover_file = open(cover_file_path, "wb")
    cover_file.write(response.content)
    cover_file.close()
    print 'Saved album cover to {0}'.format(cover_file_path)
    return cover_file_path


def get_tracks(album):
    spotify = spotipy.Spotify()
    tracks = PagedResult(spotify, spotify.album_tracks(album['id'])).get_items()
    return tracks


def cut_album(audio_file_path, cover_file_path, artist_name, album):
    # Load the audio
    print 'Loading {0}'.format(audio_file_path)
    audio = AudioSegment.from_file(audio_file_path, format="wav")

    duration_in_ms = len(audio)
    seconds = (duration_in_ms / 1000) % 60
    minutes = (duration_in_ms / (1000 * 60)) % 60
    hours = (duration_in_ms / (1000 * 60 * 60)) % 24
    print 'Audio duration: {0:02d}:{1:02d}:{2:02d}'.format(hours, minutes, seconds)

    # Write the tracks
    tracks = get_tracks(album)
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
                                         tags={'album': album['name'].encode('utf-8'), 'artist': artist_name, 'track': track_index},
                                         cover=cover_file_path)

        track_index += 1
        start_duration += track_duration

        if start_duration > len(audio):
            print 'Audio file {0} is too short, terminating'.format(audio_file_path)
            return False

    print('All tracks exported successfully')
    return True


class ExtendedSpotify(spotipy.Spotify):
    def me_player_devices(self):
        ''' Get detailed profile information about the current user.
            An alias for the 'current_user' method.
        '''
        return self._get('me/player/devices')

    def me_player_play(self, device_id, data):
        return self._put('me/player/play?device_id={0}'.format(device_id), payload=data)

    def me_player_pause(self, device_id):
        return self._put('me/player/pause?device_id={0}'.format(device_id))

def get_device_names():
    scopes = [
        'user-read-playback-state', 'user-modify-playback-state'
    ]
    token = util.prompt_for_user_token(username=username, scope=' '.join(scopes),
                                       client_id=client_id,
                                       client_secret=client_secret,
                                       redirect_uri=redirect_uri)

    spotify = ExtendedSpotify(auth=token)
    return spotify.me_player_devices()

def play_album(album, device_name):
    scopes = [
        'user-read-playback-state', 'user-modify-playback-state'
    ]
    token = util.prompt_for_user_token(username=username, scope=' '.join(scopes),
                                       client_id=client_id,
                                       client_secret=client_secret,
                                       redirect_uri=redirect_uri)

    spotify = ExtendedSpotify(auth=token)
    devices = spotify.me_player_devices().get('devices', None) or []
    my_device = next(iter([device for device in devices if device['name'].encode('utf-8') == device_name]), None)
    if not my_device:
        print('Could not find device: {0}'.format(device_name))
        return None

    data = {
        'context_uri': 'spotify:album:{0}'.format(album['id']),
        'offset': {
            'position': 0
        }
    }
    return spotify.me_player_play(my_device['id'], data)


def pause_playback(device_name):
    scopes = [
        'user-read-playback-state', 'user-modify-playback-state'
    ]
    token = util.prompt_for_user_token(username=username, scope=' '.join(scopes),
                                       client_id=client_id,
                                       client_secret=client_secret,
                                       redirect_uri=redirect_uri)

    spotify = ExtendedSpotify(auth=token)
    devices = spotify.me_player_devices().get('devices', None) or []
    my_device = next(iter([device for device in devices if device['name'].encode('utf-8') == device_name]), None)
    if not my_device:
        print('Could not find device: {0}'.format(device_name))
        return None

    return spotify.me_player_pause(my_device['id'])


if __name__ == "__main__":
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
    artist_url = get_artist_url(artist_name)
    if not artist_url:
        print 'Artist {0} not found'.format(artist_name)
        exit()
    print 'Artist found with Spotify: {0}'.format(artist_url)

    # Get the album
    album = get_album(artist_url, album_name, market)
    if not album:
        exit()

    # Get the cover
    save_cover(album, os.path.dirname(audio_file_path))

    # Cut the wav
    cut_album(audio_file_path, album)
