# coding: utf-8
import spotify
from record import Recorder
from datetime import datetime
from datetime import timedelta
from slugify import slugify
import socket

def stream_album(artist_name, album_name, recording_device_index):
    artist_url = spotify.get_artist_url(artist_name)
    if not artist_url:
        print('Artist {0} not found'.format(artist_name))
        exit()

    album = spotify.get_album(artist_url, album_name, 'NL')
    if not album:
        return False

    cover_file_path = spotify.save_cover(album, '.')

    tracks = spotify.get_tracks(album)
    total_time_ms = sum([track['duration_ms'] for track in tracks])
    stop_date_time = datetime.now() + timedelta(
        milliseconds=total_time_ms + 5000)  # Add an extra 5s to be sure we capture the whole album
    #stop_date_time = datetime.now() + timedelta(milliseconds=5000)


    # Get the wav
    audio_file_path = '{0}.wav'.format(slugify(album_name))

    device_name = socket.gethostname()
    spotify.play_album(album, device_name=device_name)
    print('Started playback of Spotify album')
    #recorder = Recorder(audio_file_path,device_index=3)
    recorder = Recorder(audio_file_path,device_index=recording_device_index)
    recorder.record_until(stop_date_time)

    spotify.pause_playback(device_name=device_name)


    # Now
    return spotify.cut_album(audio_file_path, cover_file_path, artist_name, album)

if __name__ == "__main__":
    print(Recorder.query_devices())
    #device_names = spotify.get_device_names()
    #pass
    stream_album('Rowwen Heze', "Kilomeaters ('T Beste Van 20 Joar Rowwen Hèze)", 1)
