# coding: utf-8

import spotify
import albumcut

albums = spotify.get_my_albums()
print ('The following albums will be streamed\n{0}'.format('\n'.join([album['album']['name'].encode('utf-8') for album in albums['items']])))
for album in albums['items']:
    album = album['album']
    album_name = album['name'].encode('utf-8')

    artist = next(iter(album['artists']), None)
    if not artist:
        print 'No artist found for album {0}'.format(album_name)

    artist_name = artist['name'].encode('utf-8')

    print('Streaming album {0}, artist={1}'.format(album_name, artist_name))
    albumcut.stream_album(recording_device_index=3, album_id = album['id'].encode('utf-8'), artist_name=artist_name)
