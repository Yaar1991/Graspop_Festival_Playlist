#  Copyright (c) 2023. Lorem ipsum dolor sit amet, consectetur adipiscing elit.
#  Morbi non lorem porttitor neque feugiat blandit. Ut vitae ipsum eget quam lacinia accumsan.
#  Etiam sed turpis ac ipsum condimentum fringilla. Maecenas magna.
#  Proin dapibus sapien vel ante. Aliquam erat volutpat. Pellentesque sagittis ligula eget metus.
#  Vestibulum commodo. Ut rhoncus gravida arcu.

import requests, json
from bs4 import BeautifulSoup

spotify_api_url = 'https://api.spotify.com/v1/'

def get_artist_id(artist_name, access_token):
    """
    Searches the Spotify API for an artist by name and returns the Spotify ID of the top result.

    Parameters:
    -----------
    artist_name : str
        The name of the artist to search for.
    ACCESS_TOKEN : str
        A valid Spotify access token to authorize the API request.

    Returns:
    --------
    str
        The Spotify ID of the top result for the provided artist name, as returned by the Spotify API search endpoint.
    """
    search_url = f"{spotify_api_url}search?q={artist_name}&type=artist&limit=1"
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(search_url, headers=headers)
    response_json = response.json()
    artist_id = response_json['artists']['items'][0]['id']

    return artist_id

def get_top_tracks(artist_id,access_token):
    """
    Returns a list of the top tracks for a given Spotify artist ID, as determined by Spotify's algorithm based on popularity in the US.

    Parameters:
    -----------
    artist_id : str
        The Spotify ID of the artist whose top tracks should be returned.

    Returns:
    --------
    list of dicts
        A list of dictionaries representing the top tracks for the given artist, as returned by the Spotify API.
    """
    top_tracks_url = f"{spotify_api_url}artists/{artist_id}/top-tracks?country=US"
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(top_tracks_url, headers=headers)
    response_json = response.json()
    top_tracks = response_json['tracks']
    return top_tracks

def get_artists_from_festival(graspop_url):
    """
    Extracts the names of all artists performing at a festival from the provided graspop_url.

    Parameters:
    -----------
    graspop_url : str
        The URL of the festival lineup page to extract artist names from.

    Returns:
    --------
    list of str
        The names of all artists performing at the festival, extracted from the HTML content of the provided URL.
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
