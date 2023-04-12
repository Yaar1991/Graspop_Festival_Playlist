import requests,json
from Spotify_Playlist_creation import Graspop_Artists


def getPlaylistID():
    """
    Prompts the user for input to determine whether they already have a Spotify playlist ID, and if so, returns that ID as a string. If the user does not have a playlist or chooses not to provide an ID, None is returned.

    Returns:
    --------
    str or None
        The Spotify playlist ID entered by the user, or None if no ID is provided.
    """
    is_PLAYLIST = input("Do you have a Playlist?")
    if is_PLAYLIST == 'Yes':
        PLAYLIST_ID = input("If you already have a playlist, put its ID here: ")
    else:
        PLAYLIST_ID = None
    return PLAYLIST_ID

def create_playlist(SP_Object,playlist_name):
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
    user_id = SP_Object.me()['id']
    playlist_id = SP_Object.user_playlist_create(user_id, playlist_name)
    return playlist_id

def add_top_track_to_playlist(Artists_Name, ACCESS_TOKEN):
    """
    Given a list of artist names, finds the top track for each artist and adds it to a Spotify playlist.

    Parameters:
    -----------
    Artists_Name : list of str
        A list of artist names to search for and add to the playlist.
    ACCESS_TOKEN : str
        A valid Spotify access token to authorize the API requests.

    Returns:
    --------
    list of str
        A list of Spotify track URIs, one for each top track found and added to the playlist.
    """
    URIList = []
    for Artist_Name in Artists_Name:
        # Get Artist ID:
        artistID = Graspop_Artists.get_artist_id(Artist_Name, ACCESS_TOKEN)

        # Get Top Tracks of the Artist
        top_tracks = Graspop_Artists.get_top_tracks(artistID, ACCESS_TOKEN)

        # Get the most played track of the artist:
        TRACK_ID = max(top_tracks, key=lambda x: x['popularity'])['id']

        # Add Top Tracks of the Artist to the Tracks URI
        URIList.append(f"spotify:track:{TRACK_ID}")

    return URIList



def add_song_to_playlist(playlist, track_id, ACCESS_TOKEN, SPOTIFY_API_URL):
    """
    Adds a track with the given track ID to the specified playlist.

    Args:
    - playlist: a dictionary representing the playlist to which the track should be added. The dictionary should have an 'id' key with the value of the playlist ID.
    - track_id: a string representing the track ID of the track to add.
    - ACCESS_TOKEN: a string representing the access token for accessing the Spotify API.
    - SPOTIFY_API_URL: a string representing the base URL for the Spotify API.

    Returns:
    - snapshot_id: a string representing the snapshot ID of the updated playlist.
    """
    playlist_id = playlist['id']
    add_track_url = f"{SPOTIFY_API_URL}playlists/{playlist_id}/tracks"
    headers = {'Authorization': f'Bearer {ACCESS_TOKEN}', 'Content-Type': 'application/json'}
    uri = f"spotify:track:{track_id}"
    data = {'uris': [uri]}
    response = requests.post(add_track_url, headers=headers, data=json.dumps(data))

    response_json = response.json()
    snapshot_id = response_json['snapshot_id']

    return snapshot_id