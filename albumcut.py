# coding: utf-8
import spotify
from record import Recorder
from datetime import datetime
from datetime import timedelta
from slugify import slugify
import socket


def stream_playlist(playlist, recording_device_index=1):
    tracks = spotify.get_tracks_for_playlist(playlist)
    total_time_ms = sum([item['duration_ms'] for item in tracks])
    stop_date_time = datetime.now() + timedelta(
        milliseconds=total_time_ms + 5000)  # Add an extra 5s to be sure we capture the whole playlist

    # Get the wav
    playlist_name = playlist['name']
    audio_file_path = '{0}.wav'.format(slugify(playlist_name))


    device_name = spotify.get_active_device_name()
    if not device_name:
        print 'No active device found, play some track on your local Spotify to set it active'
        return False

    if not type(device_name) == str:
        device_name = device_name.encode('utf-8')

    spotify.play_playlist(playlist, device_name=device_name)

    print('Started playback of Spotify playlist {0}'.format(playlist_name))
    recorder = Recorder(audio_file_path, device_index=recording_device_index)
    recorder.record_until(stop_date_time)
    spotify.pause_playback(device_name=device_name)

    # Now cut in pieces
    return spotify.cut_playlist(audio_file_path, playlist)


def stream_album(artist_name=None, album_name=None, recording_device_index=1, album_id=None):
    if not album_id:
        artist_url = spotify.get_artist_url(artist_name)
        if not artist_url:
            print('Artist {0} not found'.format(artist_name))
            exit()

        album = spotify.get_album(artist_url, album_name, 'NL')
    else:
        album = spotify.get_album_by_id(album_id)
        if album:
            album_name = album['name'].encode('utf-8')

    if not album:
        return False

    cover_file_path = spotify.save_cover(album, '.')

    tracks = spotify.get_tracks(album)
    total_time_ms = sum([track['duration_ms'] for track in tracks])
    stop_date_time = datetime.now() + timedelta(
        milliseconds=total_time_ms + 5000)  # Add an extra 5s to be sure we capture the whole album
    #stop_date_time = datetime.now() + timedelta(milliseconds=5000)


    # Get the wav
    audio_file_path = '{0}.wav'.format(slugify(album_name.decode('utf-8')))

    device_name = spotify.get_active_device_name()
    if not device_name:
        print 'No active device found, play some track on your local Spotify to set it active'
        return False

    if not type(device_name) == str:
        device_name = device_name.encode('utf-8')

    spotify.play_album(album, device_name=device_name)
    print('Started playback of Spotify album')
    recorder = Recorder(audio_file_path,device_index=recording_device_index)
    recorder.record_until(stop_date_time)
    spotify.pause_playback(device_name=device_name)



    # Now cut in pieces
    return spotify.cut_album(audio_file_path, cover_file_path, artist_name, album)

if __name__ == "__main__":
    #stream_album('Rowwen Heze', "Kilomeaters ('T Beste Van 20 Joar Rowwen Hèze)", 3)
    stream_album('De Poema\'s', 'Best Of De Poema\'s', 3)
    stream_album('Veldhuis & Kemper', 'Hollandse Sterren Collectie', 3)