#  Copyright (c) 2023. Lorem ipsum dolor sit amet, consectetur adipiscing elit.
#  Morbi non lorem porttitor neque feugiat blandit. Ut vitae ipsum eget quam lacinia accumsan.
#  Etiam sed turpis ac ipsum condimentum fringilla. Maecenas magna.
#  Proin dapibus sapien vel ante. Aliquam erat volutpat. Pellentesque sagittis ligula eget metus.
#  Vestibulum commodo. Ut rhoncus gravida arcu.
import base64,requests, json

with open('config.json') as f:
    config=json.load(f)

Client_id = config['application']['id']
Client_secret = config['application']['secret']
grantType = 'client_credentials'

# Spotify API endpoints`
URLAuthBase = 'https://accounts.spotify.com'
URLToken = '/api/token'

def getToken():
    ID_Sec_64=base64.b64encode((Client_id + ':' + Client_secret).encode('ascii')).decode('ascii')
    HeadersAuth = {'Authorization': 'Basic ' + ID_Sec_64}
    bodyToken = {'grant_type':grantType}

    res=requests.request(method='POST', url = URLAuthBase+URLToken,headers=HeadersAuth,data=bodyToken)
    if res.status_code == 200:
        token = res.json().get('access_token')
        return token
    else:
        print("status code isn't 200")
        raise RuntimeError("The API request has not executed properly due to: ") from Exception