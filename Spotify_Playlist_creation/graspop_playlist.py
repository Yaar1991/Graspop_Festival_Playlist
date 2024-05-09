import requests, json
from typing import Union, Optional
from Spotify_Playlist_creation_folder import graspop_artists


def get_playlist_id() -> Union[str, None]:
    """
    The get_playlist_id() function prompts the user to enter whether they already have a playlist or not. If the user answers with "Yes" or "yes", the function prompts the user to enter the ID of the playlist. Otherwise, the function returns None. The function returns a string or None.

    Variables:

    Union: allows for specifying multiple possible return types for a function.
    The function takes no arguments and returns a string or None.
    """
    is_playlist = input("Do you have a Playlist? ")
    if is_playlist == 'Yes' or is_playlist == 'yes':
        playlist_id = input("If you already have a playlist, put its ID here: ")
    else:
        playlist_id = None
    return playlist_id


def create_playlist(sp_object: object, playlist_name: str, playList_not_null: Optional[str] = None) -> str:
    """
    The create_playlist() function creates a new playlist or uses an existing one. If playlist_name is not None,
    the function attempts to use playList_not_null as the ID of an existing playlist. Otherwise, the function creates
    a new playlist with the name input("What's your Festival name? "). The function returns the ID of the playlist as
    a string.
    ----------
    Variables:
    ----------
    Optional: allows for specifying optional arguments for a function.
    The function takes three arguments: sp_object, which is a Spotify object; playlist_name, which is a string
    representing the name of a new playlist; and playList_not_null, which is an optional string representing the ID
    of an existing playlist. The function returns a string.
    """
    user_id = sp_object.me()['id']
    if playlist_name:
        return playList_not_null
    else:
        playlist_ = sp_object.user_playlist_create(user_id, input("What's your Playlist name? "))
        return playlist_


def add_top_track_to_playlist(artists_name: list[str], access_token: str) -> list[str]:
    """
    The add_top_track_to_playlist() function takes a list of artist names and an access token as input and returns a
    list of Spotify track URIs.

    For each artist name in the input list, the function retrieves the artist's ID using the get_artist_id() function
    from the graspop_artists module. It then retrieves the artist's top tracks using the get_top_tracks() function from the same module and selects the most popular track by popularity score. Finally, the function constructs a Spotify track URI for the selected track and appends it to the output list.

    Variables:

    list[str]: a list of strings.
    lambda: a Python keyword that is used to define anonymous functions.
    The function takes two arguments: artists_name, which is a list of strings representing artist names;
    and access_token, which is a string representing the access token for the Spotify API.
    The function returns a list of strings representing Spotify track URIs.
    """
    url_list = []
    for artist_name in artists_name:
        # Get Artist ID:
        artist_id = graspop_artists.get_artist_id(artist_name, access_token)
        if artist_id == '6hYrMIagu9UiIJc7bME1gX' or artist_id == '1Un7KYp1I6P29gkp9u9Bhh':
            continue

        # Get Top Tracks of the Artist
        top_tracks = graspop_artists.get_top_tracks(artist_id, access_token)

        # Get the most played track of the artist:
        track_id = max(top_tracks, key=lambda x: x['popularity'])['id']

        # Add Top Tracks of the Artist to the Tracks URI
        url_list.append(f"spotify:track:{track_id}")

    return url_list


def add_song_to_playlist(playlist: dict, track_id: str, access_token: str, spotify_api_url: str) -> str:
    """
    The add_song_to_playlist() function adds a song to a Spotify playlist. The function takes a dictionary playlist representing a playlist, a string track_id representing the ID of the track to add, a string access_token representing an access token for the Spotify API, and a string spotify_api_url representing the base URL for the Spotify API. The function returns a string representing a snapshot ID.

    The function constructs a URL for adding tracks to the playlist and creates a header with the access token. It then creates a data object with a Spotify track URI and sends an HTTP POST request to the Spotify API with the URL, header, and data objects. The function extracts the snapshot ID from the response JSON object and returns it.
    ----------
    Variables:
    ----------
    dict: a built-in Python data type representing a dictionary of key-value pairs.
    str: a built-in Python data type representing a string.
    requests: a Python library for making HTTP requests.
    json: a Python library for working with JSON data.
    --------
    The function takes four arguments: playlist, which is a dictionary representing a playlist;
    track_id, which is a string representing the ID of the track to add to the playlist;
    access_token, which is a string representing an access token for the Spotify API;
    and spotify_api_url, which is a string representing the base URL for the Spotify API.

    --------
    Returns:
    --------

    The function returns a string representing a snapshot ID.
    """
    playlist_id = playlist['id']
    add_track_url = f"{spotify_api_url}playlists/{playlist_id}/tracks"
    headers = {'Authorization': f'Bearer {access_token}', 'Content-Type': 'application/json'}
    uri = f"spotify:track:{track_id}"
    data = {'uris': [uri]}
    response = requests.post(add_track_url, headers=headers, data=json.dumps(data))

    response_json = response.json()
    snapshot_id = response_json['snapshot_id']

    return snapshot_id
