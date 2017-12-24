# coding: utf-8

import spotify
import albumcut

playlist = spotify.get_my_playlist('CD resa')
albumcut.stream_playlist(playlist, recording_device_index=3)
