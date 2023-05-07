"""
This script interacts with the Spotify API to create a playlist and add top tracks of artists who are performing in Graspop Metal Meeting festival. It uses the Spotipy library to authenticate the user's Spotify account and perform the necessary actions.

The script reads from a JSON configuration file that contains the credentials and settings required to interact with the Spotify API.

Functions:

No explicit functions are defined in this script. Instead, it imports and uses functions from other modules that are defined in the following files:

graspop_auth.py: Contains a function to authenticate with the Spotify API and retrieve an access token.

graspop_artists.py: Contains functions to extract the artist names and top tracks from the Graspop festival website, as well as to get the artist ID from the Spotify API.

graspop_playlist.py: Contains functions to create a new playlist, retrieve an existing playlist, add tracks to a playlist, and check if a playlist is empty.

:parameter:

config (dict): A dictionary that contains the Spotify application credentials and user account ID.

graspop_url (str): A string that contains the URL of the Graspop festival website.

spotify_api_url (str): A string that contains the base URL of the Spotify API.

client_id (str): A string that contains the client ID of the Spotify application.

client_secret (str): A string that contains the client secret of the Spotify application.

user_id (str): A string that contains the user ID of the Spotify account.

access_token (str): A string that contains the access token of the authenticated user.

artist_name (lambda function): A lambda function that prompts the user to enter the artist names.

scopes (list): A list of strings that contains the Spotify API scopes required by the application.

encoding_type (str): A string that contains the content type of the HTTP requests.

redirect_uri (str): A string that contains the redirect URI of the Spotify application.

headers_auth (None): A None value that will be used to store the authentication headers.

sp (Spotipy object): A Spotipy object that is used to interact with the Spotify API.

playList_not_null (str): A string that contains the ID of an existing playlist.

artists_names (list): A list of strings that contains the names of the artists performing in the Graspop festival.

song_list (list): A list of strings that contains the top tracks of the artists in the Graspop festival.

playlist (dict): A dictionary that contains the ID of the created playlist.

snapshot_id (list): A list of strings that contains the snapshot ID of the updated playlist.
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
