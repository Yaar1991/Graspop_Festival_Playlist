import requests, json, base64, spotipy
from spotipy.oauth2 import SpotifyOAuth
from bs4 import BeautifulSoup

## Variables
# Graspop Variables
Graspop_URL = 'https://www.graspop.be/en/line-up/lijst'

# Spotify API endpoints
URLAuthBase = 'https://accounts.spotify.com'
SPOTIFY_API_URL = 'https://api.spotify.com/v1/'
URLAuth = '/authorize'
URLToken = '/api/token'

# Spotify Application credentials
Client_id = 'APPS-CLIENT-ID'
Client_secret = '<APPS-CLIENT-SECRET>'

# User's Spotify ID and Access Token
USER_ID = '<YOUR-USER-ID>'
ACCESS_TOKEN = None

# Artist's Names
Artist_Name = input("Enter Artist names: ")

# Spotify Application parameters
PLAYLIST_ID = input("If you already have a playlist, put it here: ")
scopes = 'user-read-email user-read-private playlist-modify-private playlist-modify-public playlist-read-private ' \
         'app-remote-control playlist-read-collaborative'
encodingType = 'application/x-www-form-urlencoded'
URIList = []


redirect_uri = 'http://127.0.0.1:9090'
grantType = 'client_credentials'
baseString64 = None
HeadersAuth = None
ParamsAuth = None

# Get Spotipy Object
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=Client_id,
                                               client_secret=Client_secret,
                                               redirect_uri=redirect_uri,
                                               scope=scopes))


# Get Access Token
def getToken():
    baseString64=Client_id + ':' + Client_secret
    baseString64=base64.b64encode(baseString64.encode("ascii")).decode("ascii")
    ID_Sec_64=base64.b64encode((Client_id + ':' + Client_secret).encode('ascii')).decode('ascii')
    HeadersAuth = {'Authorization': 'Basic ' + ID_Sec_64}
    bodyToken = {'grant_type':grantType}

    res=requests.request(method='POST', url = URLAuthBase+URLToken,headers=HeadersAuth,data=bodyToken)
    if res.status_code == 200:
        token = res.json().get('access_token')
        return token
    else:
        print("status code isn't 200")
        raise Exception

# Search the Artist and get their ID:
def get_artist_id(artist_name):
    search_url = f"{SPOTIFY_API_URL}search?q={artist_name}&type=artist&limit=1"
    headers = {'Authorization': f'Bearer {ACCESS_TOKEN}'}

    response = requests.get(search_url, headers=headers)
    response_json = response.json()
    artist_id = response_json['artists']['items'][0]['id']

    return artist_id

# Search Artist's top song:
def get_top_tracks(artist_id):
    top_tracks_url = f"{SPOTIFY_API_URL}artists/{artist_id}/top-tracks?country=US"
    headers = {'Authorization': f'Bearer {ACCESS_TOKEN}'}

    response = requests.get(top_tracks_url, headers=headers)
    response_json = response.json()
    top_tracks = response_json['tracks']

    return top_tracks

# Create a new playlist
def create_playlist(playlist_name):
    # playlist_url = f"{SPOTIFY_API_URL}users/{USER_ID}/playlists"
    # headers = {'Authorization': f'Bearer {ACCESS_TOKEN}', 'Content-Type': 'application/json'}

    # data = {'name': playlist_name, 'public': True}
    user_id=sp.me()['id']
    # playlists = sp.current_user_playlists()
    playlist_idd=sp.user_playlist_create(user_id,playlist_name)
    # response = requests.post(playlist_url, headers=headers, data=json.dumps(data))

    # response_json = response.json()
    # playlist_id = response_json['id']

    return playlist_idd

# Add the most played song to the playlist
def add_song_to_playlist(playlist, track_id):
    playlist_id = playlist['id']
    add_track_url = f"{SPOTIFY_API_URL}playlists/{playlist_id}/tracks"
    headers = {'Authorization': f'Bearer {ACCESS_TOKEN}', 'Content-Type': 'application/json'}
    uri = f"spotify:track:{track_id}"

    data = {'uris': [f"spotify:track:{track_id}"]}


    response = requests.post(add_track_url, headers=headers, data=json.dumps(data))

    response_json = response.json()
    snapshot_id = response_json['snapshot_id']

    return snapshot_id

# Add the top track of the Artist to the playlist
def add_top_track_to_playlist(Artists_Name):
    # : Artists_Name is a list of Artists
    # : PLAYLIST_ID is the Playlist ID

    for Artist_Name in Artists_Name:
        # Get Artist ID:
        artistID = get_artist_id(Artist_Name)

        # Get Top Tracks of the Artist
        top_tracks = get_top_tracks(artistID)

        # Get the most played track of the artist:
        TRACK_ID=max(top_tracks, key=lambda x: x['popularity'])['id']

        # Add Top Tracks of the Artist to the Tracks URI
        URIList.append(f"spotify:track:{TRACK_ID}")

    return URIList;


def get_artists(Graspop_URL): # Dafna Libis :C:
    response = requests.get(Graspop_URL)

    # Parse the HTML content using Beautiful Soup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract all the data from the selector
    data = []
    for item in soup.select(".artist__name"):
        data.append(item.text)
    return data


if __name__ == '__main__':
    # Get Access Token
    ACCESS_TOKEN = getToken()

    if PLAYLIST_ID:
        # Getting the artists name from Graspop Website
        PLAYLIST = create_playlist("Graspop 2023 - Warming Up")
        Artists_names = get_artists(Graspop_URL)
        # Getting the artists' top tracks and putting them in a list
        Song_List = add_top_track_to_playlist(Artists_names)

        # There is a limitation for sending 100 songs per request,
        # so we divide it to the first 100, and from the 100th object
        # to the last object:

        # Adding the tracks to the playlist
        snapshot_id = [sp.playlist_add_items(PLAYLIST['id'], Song_List[:99]),
                       sp.playlist_add_items(PLAYLIST['id'], Song_List[99:])]
    else:
        # Get Artist ID:
        artistID = get_artist_id(Artist_Name)

        # Create a Playlist
        PLAYLIST_ID = create_playlist("Graspop 2023 - Warming Up")
        print(PLAYLIST_ID['id'])
        # Get Top Tracks of the Artist
        top_tracks = get_top_tracks(artistID)

        # Get the most played track of the artist:
        TRACK_ID=max(top_tracks, key=lambda x: x['popularity'])['id']
        uri = [f"spotify:track:{TRACK_ID}"]

        # Add Top Tracks of the Artist to the Playlist
        #args = get_args(uri,PLAYLIST_ID)
        snapshot_id = sp.playlist_add_items(PLAYLIST_ID['id'], uri)

        print(PLAYLIST_ID['id'])
    print(PLAYLIST_ID['id'])