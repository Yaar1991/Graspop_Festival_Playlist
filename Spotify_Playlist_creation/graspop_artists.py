import requests, json
from bs4 import BeautifulSoup

spotify_api_url = 'https://api.spotify.com/v1/'

def get_artist_id(artist_name:str, access_token:str) -> str:
    """
    This function takes an artist name and an access token as input and returns the Spotify ID of the artist.
    :param artist_name (str): The name of the artist to search for.
    :param access_token (str): The access token required for the API request.
    :return: artist_id (str): The Spotify ID of the artist.
    """
    search_url = f"{spotify_api_url}search?q={artist_name}&type=artist&limit=1"
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(search_url, headers=headers)
    response_json = response.json()
    artist_id = response_json['artists']['items'][0]['id']
    return artist_id

def get_top_tracks(artist_id: str,access_token: str) -> list[dict]:
    """
    This function takes an artist's ID and an access token as input and returns a list of dictionaries, where each dictionary represents a track object. The dictionaries contain various details about the track such as track name, popularity, and preview URL. The function sends an API request to Spotify's API to retrieve the top tracks of the given artist in the US.

    Variables:

    artist_id (str): The unique identifier for the artist.
    access_token (str): A string containing a valid access token for accessing the Spotify API.
    Returns:

    top_tracks (list of dicts): A list of dictionaries where each dictionary contains information about a top track for the given artist.
    """
    top_tracks_url = f"{spotify_api_url}artists/{artist_id}/top-tracks?country=US"
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(top_tracks_url, headers=headers)
    response_json = response.json()
    top_tracks = response_json['tracks']
    return top_tracks

def get_artists_from_festival(graspop_url: str) -> list[str]:
    """
    Get the list of artists performing at a festival by scraping the festival website or making an HTTP request.

    Parameters:
    graspop_url (str): The URL of the festival website.

    Returns:
    list[str]: A list of strings, which are the names of the artists performing at the festival.
    """

    festival_name = input("What festival are you interested in? ")
    data = []

    if(festival_name=="Graspop"):
        response = requests.get(graspop_url)
        # Parse the HTML content using Beautiful Soup
        soup = BeautifulSoup(response.content, 'html.parser')
        # Extract all the data from the selector
        for item in soup.select(".artist__name"):
            data.append(item.text)
    else:
        festival_url = "https://amp-prod-aeg-festivaldata.s3.amazonaws.com/app/641/cw43fqw6rt57fthu/artists.json"
        response = requests.request(method='GET', url=festival_url)
        for item in json.load(response.content):
            data.append(item.text)

    return data
