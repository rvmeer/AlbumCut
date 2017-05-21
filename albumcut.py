# coding: utf-8
import spotify
from record import Recorder
from datetime import datetime
from datetime import timedelta

def stream_album(artist_name, album_name):
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
    audio_file_path = '{0}.wav'.format(album_name)
    spotify.play_album(album, device_name='Lijn7’s MacBook Pro')
    print('Started playback of Spotify album')
    recorder = Recorder(audio_file_path,device_index=3)
    recorder.record_until(stop_date_time)

    spotify.pause_playback(device_name='Lijn7’s MacBook Pro')


    # Now
    return spotify.cut_album(audio_file_path, cover_file_path, artist_name, album)

if __name__ == "__main__":
    stream_album('Pietje', 'The Source')
    stream_album('Ayreon', 'The Human Equation')
    stream_album('Ayreon', 'Into The Electric Castle ')
