#  Copyright (c) 2023. Lorem ipsum dolor sit amet, consectetur adipiscing elit.
#  Morbi non lorem porttitor neque feugiat blandit. Ut vitae ipsum eget quam lacinia accumsan.
#  Etiam sed turpis ac ipsum condimentum fringilla. Maecenas magna.
#  Proin dapibus sapien vel ante. Aliquam erat volutpat. Pellentesque sagittis ligula eget metus.
#  Vestibulum commodo. Ut rhoncus gravida arcu.
import base64,requests, json

with open('config.json') as f:
    config=json.load(f)

client_id = config['application']['id']
client_secret = config['application']['secret']
grant_type = 'client_credentials'

# Spotify API endpoints`
url_auth_base = 'https://accounts.spotify.com'
url_token = '/api/token'

def get_token() -> str:
    """
    The get_token() function is used to get an access token from the Spotify API. The function takes no arguments and returns a string representing an access token.

    The function encodes the client ID and secret using Base64 encoding and creates headers with the encoded credentials. It then creates a body object with a grant type and sends an HTTP POST request to the Spotify API with the URL, headers, and body object. If the response status code is 200, the function extracts the access token from the response JSON object and returns it. If the status code is not 200, the function raises a runtime error with the status code.
    ---------
    Variables:
    ---------
    str: a built-in Python data type representing a string.
    base64: a built-in Python library for encoding binary data to ASCII strings.
    requests: a Python library for making HTTP requests.
    json: a Python library for working with JSON data.
    The function takes no arguments and returns a string representing an access token.
    """
    id_sec_64=base64.b64encode((client_id + ':' + client_secret).encode('ascii')).decode('ascii')
    headers_auth = {'Authorization': 'Basic ' + id_sec_64}
    body_token = {'grant_type':grant_type}
    res=requests.request(method='POST', url = url_auth_base+url_token,headers=headers_auth,data=body_token)
    if res.status_code == 200:
        token = res.json().get('access_token')
        return token
    else:
        print("status code isn't 200")
        raise RuntimeError("The API request has not executed properly due to: ") from Exception
