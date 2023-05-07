"""
This script creates a Spotify playlist for the Graspop Festival.
The playlist is created by adding the top tracks of the artists performing at the festival.
If the playlist already exists, the script adds the top tracks of the new artists added to the festival.
The Spotify access token is required to access Spotify's API.

Functions:
----------
    - main():
        This function is executed when the script is run. It gets the access token, creates the playlist,
        gets the artists' names from the Graspop website, gets their top tracks, and adds them to the playlist.

Modules:
--------
    - graspop_auth:
        This module contains the function get_token() that returns the Spotify access token required to access Spotify's API.

    - graspop_playlist:
        This module contains the following functions:
            - get_playlist_id(): Checks if the playlist already exists and returns its ID if it does.
            - create_playlist(): Creates a new playlist and returns its ID.
            - add_top_track_to_playlist(): Takes a list of artist names and access token, and returns a list of their top tracks.

    - graspop_artists:
        This module contains the following functions:
            - get_artists_from_festival(): Returns a list of artist names from the Graspop website.
            - get_artist_id(): Takes an artist name and returns its Spotify ID.
            - get_top_tracks(): Takes an artist ID and access token, and returns their top tracks.

Note: This script was created on April 12, 2023, and requires an updated version of the Spotify API and Python 3.x.
"""

import json, spotipy, graspop_auth, graspop_artists,graspop_playlist
from spotipy.oauth2 import SpotifyOAuth


## Variables

with open('config.json') as f:
    config=json.load(f)

# Graspop Variables
graspop_url = 'https://www.graspop.be/en/line-up/lijst'

# Spotify API endpoints
spotify_api_url = 'https://api.spotify.com/v1/'


# Spotify Application credentials
client_id = config['application']['id']
client_secret = config['application']['secret']

# User's Spotify ID and Access Token
user_id = config['account']['id']
access_token = None

# Artist's Names
artist_name = lambda: input("Enter Artist names: ")

# Spotify Application parameters
scopes = config['application']['scopes']
encoding_type = 'application/x-www-form-urlencoded'

redirect_uri = config['application']['uri']
headers_auth = None

# Create Spotipy Object
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                               client_secret=client_secret,
                                               redirect_uri=redirect_uri,
                                               scope=scopes))


if __name__ == '__main__':
    # Get Access Token
    access_token = graspop_auth.get_token()
    playList_not_null=graspop_playlist.get_playlist_id()
    if playList_not_null:
        #playlist = graspop_playlist.create_playlist(sp,playList_not_null)
        artists_names = graspop_artists.get_artists_from_festival(graspop_url)
        song_list = graspop_playlist.add_top_track_to_playlist(artists_names,access_token)

        # There is a limitation for sending 100 songs per request,
        # so we divide it to the first 100, and from the 100th object
        # to the last object:
        playlist = {"id": playList_not_null}
        snapshot_id = [sp.user_playlist_add_tracks(user_id,playList_not_null, song_list[:99]),
                       sp.user_playlist_add_tracks(user_id,playList_not_null, song_list[99:],position=100)]
    else:
        artist_id = graspop_artists.get_artist_id(artist_name(),access_token)
        playlist = graspop_playlist.create_playlist(sp,None)
        top_tracks = graspop_artists.get_top_tracks(artist_id,access_token)
        track_id=max(top_tracks, key=lambda x: x['popularity'])['id']
        uri = [f"spotify:track:{track_id}"]
        snapshot_id = sp.playlist_add_items(playlist['id'], uri)
        print(playlist['id'])
    print(playlist['id'])
