# AlbumCut
Cuts album WAV files based on Spotify album information.

1) Make sure you stream Spotify audio of an album to a WAV file, in this case OKComputer.wav
2) Run python spotify.py --artist "Radiohead" --album "OK Computer" --audio OKComputer.wav

The tool retrieves the album information with Spotify and downloads the album cover.
Then, it creates separate MP3 files based on the track length information obtained from spotify.
The MP3 files contain ID3 info, including the album cover.

<p>
Depends on:
<ul>
<li>ffmeg (you should install this on your machine, should be in the PATH)
</ul>

<p>
Python dependencies:
<ul>
<li>requests
<li>spotipy
<li>pydub
</ul>

<p>
Use this tool for your own benefit, do not distribute the created MP3 files!