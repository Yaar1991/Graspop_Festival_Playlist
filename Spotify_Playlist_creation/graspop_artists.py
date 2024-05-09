import time
import re
import requests
from bs4 import BeautifulSoup

SPOTIFY_API_URL = 'https://api.spotify.com/v1/'


def get_artist_id(artist_name: str, access_token: str) -> str:
    """
    This function takes an artist name and an access token as input and returns the Spotify ID of the artist.
    :param artist_name: The name of the artist to search for.
    :param access_token: The access token required for the API request.
    :return: artist_id (str): The Spotify ID of the artist.
    """
    search_url = f"{SPOTIFY_API_URL}search?q={artist_name}&type=artist&limit=1"
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(search_url, headers=headers)

    response_json = response.json()
    artist_id = response_json['artists']['items'][0]['id']
    return artist_id


def get_top_tracks(artist_id: str, access_token: str) -> list[dict]:
    """
    This function takes an artist's ID and an access token as input and returns a list of dictionaries,
    where each dictionary represents a track object. The dictionaries contain various details about the track such as
    track name, popularity, and preview URL.
     The function sends an API request to Spotify's API to retrieve the top tracks of the given artist in the US.

    Variables:

    artist_id (str): The unique identifier for the artist.
    access_token (str): A string containing a valid access token for accessing the Spotify API.
    Returns:

    top_tracks (list of dicts): A list of dictionaries where each dictionary contains information about a top track for
     the given artist.
    """
    top_tracks_url = f"{SPOTIFY_API_URL}artists/{artist_id}/top-tracks?country=US"
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(top_tracks_url, headers=headers)
    response_json = response.json()
    top_tracks = response_json['tracks']
    if not top_tracks:
        time.sleep(3)
        top_tracks_url_GB = f"{SPOTIFY_API_URL}artists/{artist_id}/top-tracks?country=GB"
        try:
            response = requests.get(top_tracks_url_GB, headers=headers)
        except ValueError as e:
            print(f"Value Error: {e}")
        response_json = response.json()
        top_tracks = response_json['tracks']
        if top_tracks:
            return top_tracks
        else: # France
            time.sleep(3)
            top_tracks_url_DE = f"{SPOTIFY_API_URL}artists/{artist_id}/top-tracks?country=DE"
            try:
                response = requests.get(top_tracks_url_DE, headers=headers)
            except ValueError as e:
                print(f"Value Error: {e}")
            response_json = response.json()
            top_tracks = response_json['tracks']
            if top_tracks:
                return top_tracks
            else: # France
                time.sleep(3)
                top_tracks_url_FR = f"{SPOTIFY_API_URL}artists/{artist_id}/top-tracks?country=FR"
                try:
                    response = requests.get(top_tracks_url_FR, headers=headers)
                except ValueError as e:
                    print(f"Value Error: {e}")
                response_json = response.json()
                top_tracks = response_json['tracks']
                if top_tracks:
                    return top_tracks
                else: # Turkey
                    time.sleep(3)
                    top_tracks_url_TR = f"{SPOTIFY_API_URL}artists/{artist_id}/top-tracks?country=TR"
                    try:
                        response = requests.get(top_tracks_url_TR, headers=headers)
                    except ValueError as e:
                        print(f"Value Error: {e}")
                    response_json = response.json()
                    top_tracks = response_json['tracks']
                    if top_tracks:
                        return top_tracks
    return top_tracks


def get_artists_from_festival(festival_url: str) -> list[str]:
    """
    Get the list of artists performing at a festival by scraping the festival website or making an HTTP request.

    Parameters:
    graspop_url (str): The URL of the festival website.
    Returns:
    list[str]: A list of strings, which are the names of the artists performing at the festival.
    """

    festival_name = input("What festival are you interested in? ")
    data = []

    if festival_name == "Graspop":
        response = requests.get(festival_url)
        # Parse the HTML content using Beautiful Soup
        soup = BeautifulSoup(response.content, 'html.parser')
        # Extract all the data from the selector
        for item in soup.select(".artist__name"):
            data.append(item.text)
    else:  # Hellfest
        response = requests.get('https://hellfest.fr/en/line-up/')
        # Parse the HTML content using Beautiful Soup
        soup = BeautifulSoup(response.content, 'html.parser')
        # Extract the relevant portion of the text
        relevant_text = re.search(r'Temple(.*?)Contact', soup.text, re.DOTALL).group(1)
        pattern = re.compile(r"^([A-Z0-9\s&'.]+)$", re.MULTILINE)
        # Find all the names using regular expression.
        # We look for text that follows the pattern after † symbols.
        # Finding all matches in the text
        bands = pattern.findall(relevant_text)
        # Clean up and filter out any empty entries
        names = [name.strip() for name in bands if (name.strip() and len(name) > 0)]
        bandit = [names[index].replace('\n\n\n\n', '\n\n\n').replace('\n\n\n', '\n\n').replace('\n\n', ',').split(',')
                  for index
                  in range(0, len(names))]
        len_bandit = len(bandit)
        data = []
        for i in range(0, len_bandit):
            for j in range(0, len(bandit[i])):
                data.append(bandit[i][j])
    return data
