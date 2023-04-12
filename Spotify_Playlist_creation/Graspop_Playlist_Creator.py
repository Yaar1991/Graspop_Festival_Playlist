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
    - Graspop_Auth:
        This module contains the function getToken() that returns the Spotify access token required to access Spotify's API.

    - Graspop_Playlist:
        This module contains the following functions:
            - getPlaylistID(): Checks if the playlist already exists and returns its ID if it does.
            - create_playlist(): Creates a new playlist and returns its ID.
            - add_top_track_to_playlist(): Takes a list of artist names and access token, and returns a list of their top tracks.

    - Graspop_Artists:
        This module contains the following functions:
            - get_artists_from_Festival(): Returns a list of artist names from the Graspop website.
            - get_artist_id(): Takes an artist name and returns its Spotify ID.
            - get_top_tracks(): Takes an artist ID and access token, and returns their top tracks.

Note: This script was created on April 12, 2023, and requires an updated version of the Spotify API and Python 3.x.
"""

import json, spotipy, Graspop_Auth, Graspop_Artists,Graspop_Playlist
from spotipy.oauth2 import SpotifyOAuth


## Variables

with open('config.json') as f:
    config=json.load(f)

# Graspop Variables
Graspop_URL = 'https://www.graspop.be/en/line-up/lijst'

# Spotify API endpoints
SPOTIFY_API_URL = 'https://api.spotify.com/v1/'


# Spotify Application credentials
Client_id = config['application']['id']
Client_secret = config['application']['secret']

# User's Spotify ID and Access Token
USER_ID = config['account']['id']
ACCESS_TOKEN = None

# Artist's Names
ArtistName = lambda: input("Enter Artist names: ")

# Spotify Application parameters
scopes = config['application']['scopes']
encodingType = 'application/x-www-form-urlencoded'

redirect_uri = config['application']['uri']
HeadersAuth = None

# Create Spotipy Object
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=Client_id,
                                               client_secret=Client_secret,
                                               redirect_uri=redirect_uri,
                                               scope=scopes))


if __name__ == '__main__':
    # Get Access Token
    ACCESS_TOKEN = Graspop_Auth.getToken()

    if Graspop_Playlist.getPlaylistID():
        # Getting the artists name from Graspop Website
        PLAYLIST = Graspop_Playlist.create_playlist(sp,"Graspop 2023 - Warming Up")
        Artists_names = Graspop_Artists.get_artists_from_Festival(Graspop_URL)
        # Getting the artists' top tracks and putting them in a list
        Song_List = Graspop_Playlist.add_top_track_to_playlist(Artists_names,ACCESS_TOKEN)

        # There is a limitation for sending 100 songs per request,
        # so we divide it to the first 100, and from the 100th object
        # to the last object:

        # Adding the tracks to the playlist
        snapshot_id = [sp.playlist_add_items(PLAYLIST['id'], Song_List[:99]),
                       sp.playlist_add_items(PLAYLIST['id'], Song_List[99:])]
    else:
        # Get Artist ID:
        artistID = Graspop_Artists.get_artist_id(ArtistName())
        # Create a Playlist
        PLAYLIST_ID = Graspop_Playlist.create_playlist("Graspop 2023 - Warming Up")
        print(PLAYLIST_ID['id'])
        # Get Top Tracks of the Artist
        top_tracks = Graspop_Artists.get_top_tracks(artistID,ACCESS_TOKEN)
        # Get the most played track of the artist:
        TRACK_ID=max(top_tracks, key=lambda x: x['popularity'])['id']
        uri = [f"spotify:track:{TRACK_ID}"]
        # Add Top Tracks of the Artist to the Playlist
        snapshot_id = sp.playlist_add_items(PLAYLIST_ID['id'], uri)

        print(PLAYLIST_ID['id'])
    print(PLAYLIST_ID['id'])
