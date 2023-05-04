import requests,json
from Spotify_Playlist_creation import graspop_artists


def get_playlist_id():
    """
    Prompts the user for input to determine whether they already have a Spotify playlist ID, and if so, returns that ID as a string. If the user does not have a playlist or chooses not to provide an ID, None is returned.

    Returns:
    --------
    str or None
        The Spotify playlist ID entered by the user, or None if no ID is provided.
    """
    is_playlist = input("Do you have a Playlist?")
    if is_playlist == 'Yes':
        playlist_id = input("If you already have a playlist, put its ID here: ")
    else:
        playlist_id = None
    return playlist_id

def create_playlist(sp_object,playlist_name):
    """
    Creates a new Spotify playlist with the given name, belonging to the current user, using the Spotify Web API.

    Parameters:
    -----------
    playlist_name : str
        The name of the playlist to be created.

    Returns:
    --------
    str
        The unique ID of the newly created playlist, as returned by the Spotify API.
    """
    user_id = sp_object.me()['id']
    playlist_id = sp_object.user_playlist_create(user_id, playlist_name)
    return playlist_id

def add_top_track_to_playlist(artists_name, access_token):
    """
    Given a list of artist names, finds the top track for each artist and adds it to a Spotify playlist.

    Parameters:
    -----------
    artists_name : list of str
        A list of artist names to search for and add to the playlist.
    access_token : str
        A valid Spotify access token to authorize the API requests.

    Returns:
    --------
    list of str
        A list of Spotify track URIs, one for each top track found and added to the playlist.
    """
    url_list = []
    for artist_name in artists_name:
        # Get Artist ID:
        artist_id = graspop_artists.get_artist_id(artist_name, access_token)

        # Get Top Tracks of the Artist
        top_tracks = graspop_artists.get_top_tracks(artist_id, access_token)

        # Get the most played track of the artist:
        track_id = max(top_tracks, key=lambda x: x['popularity'])['id']

        # Add Top Tracks of the Artist to the Tracks URI
        url_list.append(f"spotify:track:{track_id}")

    return url_list



def add_song_to_playlist(playlist, track_id, access_token, spotify_api_url):
    """
    Adds a track with the given track ID to the specified playlist.

    Args:
    - playlist: a dictionary representing the playlist to which the track should be added. The dictionary should have an 'id' key with the value of the playlist ID.
    - track_id: a string representing the track ID of the track to add.
    - access_token: a string representing the access token for accessing the Spotify API.
    - spotify_api_url: a string representing the base URL for the Spotify API.

    Returns:
    - snapshot_id: a string representing the snapshot ID of the updated playlist.
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