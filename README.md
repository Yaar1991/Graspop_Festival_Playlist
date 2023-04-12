# Graspop_Festival_Playlist
Ever wanted to go to a festival you actually know all of the bands' songs and not just a few?
Here it is! All you'll need to do is follow these steps:
## Set Up Your Account
Login to the Spotify Developer Dashboard (https://developer.spotify.com/dashboard).

## Create an app
An app provides the Client ID and Client Secret needed to request an access token by implementing any of the authorization flows.

To create an app, go to your Dashboard (https://developer.spotify.com/dashboard), click on the Create an app button and enter the following information:

* App Name: My App
* App Description: This is my first Spotify app
* Redirect URI: You won't need this parameter in this example, so simply use http://127.0.0.1:9090.

## Saving a JSON file called config.json
* Save a valid JSON file that includes the following details:

{
  "application":
    {"id": "<APP_Client_id>",
      "secret": "APP_Client_secret",
      "scopes":"Specific_Scopes_Desired",
      "uri": "http://127.0.0.1:9090"
    },
  "account":{
    "id": "<>"
  }
}
